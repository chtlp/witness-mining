import sys
from preproc import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'usage: <in-table> <out-table>'
        sys.exit(1)

    ifname = sys.argv[1]
    ifile = open(ifname)
    header = ifile.readline()

    col_names = header.strip().split('\t')
    col_proc = []
    for s in col_names:
        pn = 'proc_' + s.lower()
        if pn in globals():
            col_proc.append( globals()[pn] )
        else:
            col_proc.append( None )

    ofname = sys.argv[2]
    ofile = open(ofname, "w")

    res_cols = []
    for k, v in enumerate(col_names):
        if col_proc[k]:
            res_cols.append( v )
    ofile.write('\t'.join(res_cols) + '\n')

    for no, line in enumerate(ifile):
        values = line.strip().split('\t')
        assert len(values) == len(col_names)

        res = []
        for k, v in enumerate(values):
            if col_proc[k]:
                res.append( col_proc[k](v) )

        ofile.write('\t'.join(map(str, res)) + '\n')

    ofile.close()
                
