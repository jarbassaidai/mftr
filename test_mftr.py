# unit tests for mftr
import unittest
import multiFileTokenReplace
import argparse

"""
method to setup a parse_args value
"""
def setup_args():
    parser = argparse.ArgumentParser(description='token replace in multiple files')
    parser.add_argument('--directory', dest='dir',  default = '.', help= 'directory to run threw')
    parser.add_argument('--token',  dest='token', default = '192.168.0.0', help= 'token to look for')
    parser.add_argument('--replace', dest='replace', default = '192.168.1.1', help='replacement value' )
    parser.add_argument('--rewrite', dest='rewrite', default=True, help='allow different sized search and replace items ')
    parser.add_argument('--backup', dest='backup', default=True,  help='create backup of original file')
    parser.add_argument('--log', dest='log', default = 'mftr_change.log',  help='log file to log all changes')
    parser.add_argument('--skip', dest='skip', nargs='+', default ="png jpg exe jar z gz mftr_bck", help='list of file types that are not searched')
    parser.add_argument('--include',dest='include', nargs='+', default = '*' , help='list of file types to incluce')
    parser.add_argument('--revert',dest='revert', default = False, help='rename all the .mftr_bck files to original')
    return  parser.parse_args()


class test_compRegex(unittest.TestCase):  #unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.args = None
        self.mftr = None
        self.setup()

    def setup(self):
        self.args = setup_args()
        try:
            self.mftr = multiFileTokenReplace.multiFileTokenReplace(self.args)
        except:
            self.assertTrue(False)

    def teardown(self):
        self.args = None
        self.mftr = None

    def test_token(self):
        self.args.token = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        try:
            self.mftr.compRegx(self.args)
            match = self.mftr.token.match('234.044.1.093')
            self.assert_(match != None)
        except :
            self.assertTrue(False)

    def test_skip(self):
        try:
            match = self.mftr.skipRegex.match('thisisafilename.jpg')
            self.assert_(match != None)
            match = self.mftr.skipRegex.match('histisafilename.dat')
            self.assert_(match == None)
            match = self.mftr.skipRegex.match('histi.jpg.safilename.dat')
            self.assert_(match == None)
        except:
            self.assertTrue(False)

    def test_include(self):
        self.assertTrue(False)

class test_init(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_fileDance(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_findNReplace(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_setupRewrite(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_matchedToken(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_skip(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_include(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_revert(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)


class test_validMatchSize(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_fileAcessable(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_logMsg(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_setupChangeLog(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_logChanges(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_closeChangeLog(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

class test_arguments(unittest.TestCase):
    def test_notComplete(self):
        self.assertTrue(False)

def suite():
    suite=unittest.TestSuite()
    #suite.addTest(test_compRegex('test_notComplete'))
    suite.addTest(unittest.makeSuite(test_compRegex))
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

