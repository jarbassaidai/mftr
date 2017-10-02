#!/usr/bin/python
import sys
import os
import re
import time
import monotonic_time
from datetime import  timedelta
"""
 small program to replace in-line same sized token and replacement
  will also replace dissimilar sized items with --rewrite flag set to True

"""
#assert sys.version_info >= (3,2)

class multiFileTokenReplace:
    # called with the hash/map from  argparse
    def __init__(self, args):
        self.start_time = time.monotonic()
        self.end_time = 0
        self.rewrite = args.rewrite
        self.backup = args.backup
        self.pos = 0
        self.token = args.token
        self.replacement = args.replace
        self.setupChangeLog(args.log)
        self.lastFileChanged = None
        self.numberOfFilesChanged = 0

        # todo consider self.rewrite
        if len(args.token) == 0  :
            raise ValueError("zero length token is not allowed")
        elif len(args.replace) == 0 and not self.rewrite:
            raise ValueError("replacement length is zero not allowed")
        self.compRegx()


    def compRegx(self):
        self.token = re.compile(re.escape(self.token))
        #self.replacement = re.compile(re.escape(self.replacement))

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

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                if self.fileAcessable(filepath):
                    try:
                        if not self.blackList(filepath):
                            self.fileDance(filepath)
                    except:
                        self.logMsg('{} was not scanned \n'.format(filepath))
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
                if self.rewrite and not rewrite_setup:
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
            os.rename(file,file + '.bak' )
            old_h = open(file + '.bak',  'r')
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

    # black listed files
    # .bak, .jpg, .mp*,png, .tiff, ,.jar, .exe
    def blackList(self,file):
        rval = False
        match = re.match(r"(\.bak|\.jpg|\.mp\d|\.png|\.tiff|\.jar|\.exec)$",file)
        if match != None:
            rval = True
        return rval

    """
    checks equal size  when rewrite is not set
    also records the  line number  of the match
    """

    def validMatchSize(self,l_cnt,  line, file):
        matches= re.findall(self.token,  line)
        rval = True
        m_cnt = len(matches)
        if len(matches) and self.log_h != None:
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

    def setupChangeLog(self, logName):
        if (logName != None):
            self.log_h = open(logName, "a+") if args.log != None else None
            self.log_h.write('Start time: ' + time.strftime("%Y/%m/%d") + " "+ time.strftime("%H:%M:%S") + "\n")
            self.log_h.write('\treplace '+ self.token + ' with '  +  self.replacement + "\n")

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
    parser.add_argument('--log', dest='log', default = 'mtfp_change.log',  help='log file to log all changes')
    args = parser.parse_args()

    try:
        mftr = multiFileTokenReplace(args)
        mftr.findNReplace(args.dir)
        mftr.closeChangeLog()
    except ValueError as E:
        print(E)


    print ('done')

