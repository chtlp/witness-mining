import sys
from collections import defaultdict
import glob

if __name__ == '__main__':
    for fname in glob.glob('*.TXT'):
        print fname.replace('TXT', 'stat'),
    print

    for fname in glob.glob('*.TXT'):
        obj = fname.replace('TXT', 'stat')
        print '%s: %s' % (obj, fname)
    
        

    
