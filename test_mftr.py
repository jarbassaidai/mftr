# unit tests for mftr
import unittest
import multiFileTokenReplace
import argparse




class templateA(unittest.TestCase):
    def __init__(self,method):
        self.mftr = None
        self.setup()

    def setup(self):
        self.parser = argparse.ArgumentParser(description='token replace in multiple files')
        self.parser.add_argument('--directory', dest='dir',  required=True,  default = '.', help= 'directory to run threw')
        self.parser.add_argument('--token',  dest='token', required=True, default = 'test', help= 'token to look for')
        self.parser.add_argument('--replace', dest='replace', required=True, default = 'test', help='replacement value' )
        self.parser.add_argument('--rewrite', dest='rewrite', default=True, help='allow different sized search and replace items ')
        self.parser.add_argument('--backup', dest='backup', default=True,  help='create backup of original file')
        self.parser.add_argument('--log', dest='log', default = 'mftr_change.log',  help='log file to log all changes')
        self.parser.add_argument('--skip', dest='skip', nargs='+', help='list of file types that are not searched')
        self.parser.add_argument('--include',dest='include', nargs='+',help='list of file types to incluce')
        self.parser.add_argument('--revert',dest='revert', default = False, help='rename all the .mftr_bck files to original')
        self.args = self.parser.parse_args()
        self.mftr = multiFileTokenReplace(self.args)


    def tearDown(self):
        print('teardown\n')

class test_compRegex(templateA):  #unittest.TestCase):
    def setup(self):
        self.parser = argparse.ArgumentParser(description='token replace in multiple files')
        self.parser.add_argument('--directory', dest='dir',  required=True,  default = '.', help= 'directory to run threw')
        self.parser.add_argument('--token',  dest='token', required=True, default = '192.168.0.0', help= 'token to look for')
        self.parser.add_argument('--replace', dest='replace', required=True, default = '192.168.1.1', help='replacement value' )
        self.parser.add_argument('--rewrite', dest='rewrite', default=True, help='allow different sized search and replace items ')
        self.parser.add_argument('--backup', dest='backup', default=True,  help='create backup of original file')
        self.parser.add_argument('--log', dest='log', default = 'mftr_change.log',  help='log file to log all changes')
        self.parser.add_argument('--skip', dest='skip', nargs='+', default ='png jpg exe jar z gz mftr_bck', help='list of file types that are not searched')
        self.parser.add_argument('--include',dest='include', nargs='+', default = '*' , help='list of file types to incluce')
        self.parser.add_argument('--revert',dest='rewritevert', default = False, help='rename all the .mftr_bck files to original')
        self.args = self.parser.parse_args()
        self.mftr = None
        self.mftr = multiFileTokenReplace(self.args)

    def test_token(self):
        self.args.token = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        try:
            self.comRegx(self.args)
        except :
            self.assertTrue(False)

    def test_skip(self):
        self.assertTrue(False)

    def test_include(self):
        self.assertTrue(False)

class test_init(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_fileDance(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_findNReplace(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_setupRewrite(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_matchedToken(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_skip(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_include(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_revert(templateA):
    def test_notComplete(self):
        self.assertTrue(False)


class test_validMatchSize(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_fileAcessable(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_logMsg(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_setupChangeLog(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_logChanges(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_closeChangeLog(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

class test_arguments(templateA):
    def test_notComplete(self):
        self.assertTrue(False)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(test_compRegex('test_notComplete'))
    suite.addTest(unittest.makeSuite(test_init))
    suite.addTest(unittest.makeSuite(test_findNReplace))
    suite.addTest(unittest.makeSuite(test_fileDance))
    suite.addTest(unittest.makeSuite(test_setupRewrite))
    suite.addTest(unittest.makeSuite(test_matchedToken))
    suite.addTest(unittest.makeSuite(test_skip))
    suite.addTest(unittest.makeSuite(test_include))
    suite.addTest(unittest.makeSuite(test_revert))
    suite.addTest(unittest.makeSuite(test_validMatchSize))
    suite.addTest(unittest.makeSuite(test_fileAcessable))
    suite.addTest(unittest.makeSuite(test_logMsg))
    suite.addTest(unittest.makeSuite(test_setupChangeLog))
    suite.addTest(unittest.makeSuite(test_logChanges))
    suite.addTest(unittest.makeSuite(test_closeChangeLog))
    suite.addTest(unittest.makeSuite(test_arguments))
    return suite

# run tests
if __name__ == '__main__':
#    unittest.main()
     mySuit=suite()

     runner=unittest.TextTestRunner()
     runner.run(mySuit)

