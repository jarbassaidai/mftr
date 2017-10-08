import sys
import os
import re
import time
try:
    import monotonic_time
    from datetime import  timedelta
except  ImportError as e:
    raise ImportError('monotonic_time is a python 3.x module\n You are running {}\n{}'.format(sys.version_info,e))
"""
 small program to replace in-line same sized token and replacement
  will also replace dissimilar sized items with --rewrite flag set to True
TODO: add config file

"""

class MFTR:
    # called with the hash/map from  argparse
    def __init__(self, args):
        self.pythonVersionCheck()
        self.start_time = time.monotonic()
        self.end_time = 0
        self.rewrite = args.rewrite
        self.backup = args.backup
        self.pos = 0
        self.token = None #args.token
        self.replacement = args.replace
        self.setupChangeLog(args)
        self.lastFileChanged = None
        self.numberOfFilesChanged = 0
        self.skipRegex = None #args.skip            # should look like  "(exe|zip|tiff|)$"
        self.includeRegex = None #args.include       # should look like "(html|conf)$"
        self.revert = args.revert

        # todo consider self.rewrite
        if len(args.token) == 0  :
            raise ValueError("zero length token is not allowed")
        elif len(args.replace) == 0 and not self.rewrite:
            raise ValueError("replacement length is zero not allowed")
        self.compRegx(args)


    def pythonVersionCheck(self):
        if sys.version_info.major < 3 or   sys.version_info.minor  < 2:
            self.logMsg('python version {}.{} is below minimum required'.format(sys.version_info.major,sys.version_info.minor))
            print('python version {}.{} is below the minimum required 3.2'.format(sys.version_info.major,sys.version_info.minor))
            exit(1)
    """
    walk through lists then compile
    compile frequently used regex search tokens , token, skipType
    """
    def mkRegexOpt(self,alist):
        rval = None;
        if alist != None:
            sep = re.search('( |,)',alist)
            regex = "("
            if sep != None:
                for element in alist.split(sep.group(1)):
                    regex += '\.{}|'.format(element)
            else:
                for element in alist:
                    regex += '\.{}|'.format(element)
            regex = regex[:-1] # remove last '|'
            regex += ')$'
            rval = re.compile(regex) #re.escape(regex)  .. escapes all the special characters which we don't want
        return rval

    def compRegx(self,args):
        self.token = re.compile(args.token)  # do not escape a regular exspresion re.compile(re.escape(args.token))
         # should look like  "(exe|zip|tiff|)$"
        self.skipRegex = self.mkRegexOpt(args.skip)
        self.includeRegex = self.mkRegexOpt(args.include)

    """
    revert  all changes by renaming the  .mftr_bck files to  original
    """
    def revertFiles(self,directory):
        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                fname, ext = os.path.splitext(filename)
                if ext == '.mftr_bck':
                    # Join the two strings in order to form the full filepath.
                    new_filepath = os.path.join(root, fname)
                    old_filepath = os.path.join(root,filename)
                    try:
                        if os.path.exists(new_filepath):
                            os.remove(new_filepath)
                        os.rename(old_filepath,new_filepath)
                    except OSError as e:
                        print('failed to reiname or  remove  {} {}\n  error:{}'.format(old_filepath,new_filepath,e))
                        self.logMsg('failed to rename or  remove  {} {}\n  error:{}'.format(old_filepath,new_filepath,e))
                        continue

        self.revert == False

    def findNReplace(self, directory):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        https://stackoverflow.com/users/1779256/johnny
        https://stackoverflow.com/users/2470818/vallentin
        """
        #file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.o
        if self.revert:
            print  ('--revert switch is set to  true   exiting ' )
            exit (0)

        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                if self.fileAcessable(filepath):
                    try:
                        if self.include(filepath):  # include overrides skip,
                            self.fileDance(filepath)
                        elif  not self.skip(filepath):
                            # not on include list or no include list, and not on skip list
                            # or no skip list
                            self.fileDance(filepath)

                    except  Exception as e:
                        self.logMsg('{}\n{} was not scanned \n'.format(e, filepath))

    """
        fileDance  runs through all the lines in a file if self.rewrite is false the only same size matches and replacements
        will take place.  If rewrite is true then the original file is renamed as the backup, a new
        file with the same name is created and  all the contents to the first difference is copied over.  From that
        point all lines are copied whether or not there is any change.
    """
    def fileDance(self, file):
        fh = open(file, 'r+')
        write_fh = fh
        self.pos = fh.tell()
        line = fh.readline()
        rewrite_setup = False
        l_cnt = 0
        while len(line) > 0:
            l_cnt += 1
            if self.validMatchSize(l_cnt, line, file):
                newLine = self.matchedToken(line)
                if newLine != None and self.rewrite and not rewrite_setup:
                    # switching files
                    handlers = self.setupRewrite(file, fh, self.pos)
                    fh= handlers[0]
                    write_fh=handlers[1]
                    rewrite_setup = True

                if newLine != None:
                    write_fh.seek( self.pos, 0)
                    write_fh.write(newLine)
                    write_fh.flush()
                    os.fsync(write_fh.fileno())

            elif rewrite_setup:
                # write all lines to changed file
                write_fh.write(line)

            self.pos = fh.tell()
            line = fh.readline()  #[0:-1]
        if self.rewrite and rewrite_setup and write_fh != None and write_fh != fh:
            write_fh.close()
        fh.close()

    #  rename original to backup, create new with original name
    #  copy in x amount of unchanged data
    # old_h file pos ends up where  it was when module is called  file is now opened in 'r' mode
    # return new file handle
    def setupRewrite(self, file, old_h, count):
        new_h = old_h
        if self.backup:
            old_h.close()
            os.rename(file,file + '.mftr_bck' )
            old_h = open(file + '.mftr_bck',  'r')
            new_h = open(file, 'a+')
            old_h.seek(0, 0)
            pos = 0
            while pos > count :
                o_line = old_h.readline()
                new_h.write(o_line)
                pos = new_h.tell()
            # one more read for  to account for the line being modified
            old_h.readline()
        rval=[]
        rval.append(old_h)
        rval.append(new_h)
        return rval

    def matchedToken(self,line):
        rval = None
        if len(line) > 0:
            newLine = self.token.subn(self.replacement, line)
            rval = newLine[0]  if newLine[1] > 0 else None
        return rval

    # file types to skip
    # .mftr_bck, .jpg, .mp*,png, .tiff, ,.jar, .exe
    def skip(self,file):
        rval = False
        if (self.skipRegex != None):
            match = self.skipRegex.search(file)
            #match = re.match(self.skipRegex,file)
            if match != None:
                s1,s2 = match.span()
                if s2 - s1 > 0:
                    rval = True
                    self.logMsg('on skip list {}\n'.format(file))

        return rval

    # file types to include
    def include(self,file):
        rval = False
        if self.includeRegex != None:
            match = self.includeRegex.search(file)
            #match = re.match(self.includeRegex,file)
            if match != None:
                s1, s2 =  match.span()
                if s2 - s1 > 0:
                    rval = True
                    self.logMsg('on inlude list {} \n'.format(file))

        return rval

    """
    checks equal size  when rewrite is not set
    also records the  line number  of the match
    """

    def validMatchSize(self,l_cnt,  line, file):
        matches= re.findall(self.token,  line)
        rval = True if len(matches) > 0 else  False
        m_cnt = len(matches)
        if len(matches) > 0 and self.log_h != None:
            self.logChanges ('{}  m> '.format(l_cnt), file)

        for item in matches:
            if len(item) != len(self.replacement) and not self.rewrite:
                rval = False
                # todo consider self.rewrite
                #raise ValueError("search and replace values are not of equal length")
                self.logMsg(item + 'size is not equal to ' + self.replacement + ' in file:' + file  + "\n")
            if self.log_h != None:
                m_cnt -= 1
                self.logChanges(item + ' ', file)
                if m_cnt  == 0:
                    self.logChanges('\n', file)

        return rval

    def fileAcessable(self, file):
        rval = True
        if not os.access(file, os.R_OK | os.W_OK):
            rval = False
            self.logMsg(file + 'not accessable \n')
        return rval

    def logMsg(self, msg):
        f = open('mftr_msg.log', 'a+')
        f.write(msg)
        f.close()

    def setupChangeLog(self, args):
        if (args.log != None):
            self.log_h = open(args.log, "a+") if args.log != None else None
            self.log_h.write('Start time: ' + time.strftime("%Y/%m/%d") + " "+ time.strftime("%H:%M:%S") + "\n")
            self.log_h.write('\treplace '+ args.token + ' with '  +  args.replace + "\n")

    def logChanges(self, msg, file):
        if self.lastFileChanged == None or self.lastFileChanged != file:
            self.log_h.write("\n" + file + ":\nline  matches:\n" + msg )
            self.lastFileChanged = file
            self.numberOfFilesChanged +=1
        elif self.lastFileChanged == file:
            self.log_h.write(msg)

    def closeChangeLog(self):
        if self.log_h != None:
            self.log_h.write('\ntotal number of files changed: {}\n'.format(self.numberOfFilesChanged))
            self.log_h.write('Ending time: ' + time.strftime("%Y/%m/%d") + " "+ time.strftime("%H:%M:%S") + "\n")
            self.end_time = time.monotonic()
            self.log_h.write('Duration: {} seconds'.format(self.end_time - self.start_time) )
            self.log_h.close()
"""
example comandline
./multiFileTokenReplace --directory test --token 34.56.1.234 --replace 12.34.56.89  --skip 'jpg tiff  exe zip gz  tgz ' --include 'html'
"""

if __name__ == "__main__":
    import argparse
    print(sys.version_info)
#
    parser = argparse.ArgumentParser(description='token replace multiple files')
    parser.add_argument('--directory', dest='dir',  required=True,  help= 'directory to run threw')
    parser.add_argument('--token',  dest='token', required=True, help= 'token to look for')
    parser.add_argument('--replace', dest='replace', required=True, help='replacement value' )
    parser.add_argument('--rewrite', dest='rewrite', default=True, help='allow different sized search and replace items ')
    parser.add_argument('--backup', dest='backup', default=True,  help='create backup of original file')
    parser.add_argument('--log', dest='log', default = 'mftr_change.log',  help='log file to log all changes')
    parser.add_argument('--skip', dest='skip', nargs='*', type=str, help='list of file types that are not searched **coma** separator')
    parser.add_argument('--include',dest='include', nargs='*', type=str, help='list of file types to search **coma** separator')
    parser.add_argument('--revert',dest='revert', default = False, help='rename all the .mftr_bck files to original')
    args = parser.parse_args()

    try:
        mftr = MFTR(args)
        if args.revert == 'True':
            mftr.revertFiles(args.dir)
        else:
            mftr.findNReplace(args.dir)

        mftr.closeChangeLog()
    except ValueError as E:
        print(E)


    print ('done')

