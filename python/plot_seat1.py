from pylab import *
import numpy as np
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: <ifile>'
        sys.exit(1)

    m = loadtxt(sys.argv[1], skiprows = 1)
    
    header = open(sys.argv[1]).readline()
    cols = header.strip().split('\t')
    


    seat_col = cols.index('SEAT_POS')
    inj_col = cols.index('INJ_SEV')

    seat_map = {1: 'front-left', 2: 'front-right', 3: 'second-right', 4: 'second-left', 0: 'non-motorist'}


    for k, s in seat_map.iteritems():
        fl = m[:,seat_col] == k

        l = m[np.where(fl), inj_col][0]
        figure()
        hist(l, bins = 5)
        savefig('seat %s.png' % s)
    
