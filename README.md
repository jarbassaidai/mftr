# mftr
token replace for multiple files in python with log and backup optional 
parser = argparse.ArgumentParser(description='token replace multiple files')
    parser.add_argument('--directory', dest='dir',  required=True,  help= 'directory to run threw')
    parser.add_argument('--token',  dest='token', required=True, help= 'token to look for')
    parser.add_argument('--replace', dest='replace', required=True, help='replacement value' )
    parser.add_argument('--rewrite', dest='rewrite', default=True, help='allow different sized search and replace items ')
    parser.add_argument('--backup', dest='backup', default=True,  help='create backup of original file')
    parser.add_argument('--log', dest='log', default = 'mtfp_change.log',  help='log file to log all changes')

Not ready for prime time needs more testing !!
