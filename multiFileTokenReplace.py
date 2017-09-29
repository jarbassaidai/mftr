import os
import re

"""
 small program to replace in line same sized token and replacement 

"""

class multiFileTokenReplace:
    # called with the hash/map from  argparse 
    def __init__(self, args):
        self.rewrite = args.rewrite
        self.backup = args.backup
        self.log_h = open(args.log, "a+") if args.log != None else None
        self.pos = 0
        self.token = args.token
        self.replacement = args.replace
        self.lastFileChanged = None
        
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
                    self.fileDance(filepath)
                
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
        while len(line) > 0:
            if self.validMatchSize(line, file):
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
                    if self.log_h != None:
                        self.logChanges('oldline:\n\t' + line + 'newLine:\n\t'+ newLine, file)
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
         
    def validMatchSize(self, line, file):
        matches= re.findall(self.token,  line)
        rval = True
        for item in matches:
            if len(item) != len(self.replacement) and not self.rewrite:
                rval = False
                # todo consider self.rewrite
                #raise ValueError("search and replace values are not of equal length")
                self.logMsg(item + 'size is not equal to ' + self.replacement + ' in file:' + file  + "\n")
                
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
         
    def logChanges(self, msg, file):
        if self.lastFileChanged == None or self.lastFileChanged != file:
            self.log_h.write("\n" + file + "\n" + msg + "\n")
            self.lastFileChanged = file
        elif self.lastFileChanged == file:
            self.log_h.write(msg)
        
    def closeChangeLog(self):
        if self.log_h != None:
            self.log_h.close()
        


if __name__ == "__main__":
    import argparse
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
    
