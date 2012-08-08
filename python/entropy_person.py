import sys
import glob
from collections import defaultdict
from pylab import *

def read_col_file(fname):
    cols = {}
    ifile = open(fname)
    for line in ifile:
        if line.startswith('#') or not line.strip():
            continue

        col_name, col_values = map(lambda s: s.strip(), line.split(':'))
        if not col_values:
            cols[col_name] = None
        else:
            cols[col_name] = col_values.split('\t')

    return cols



def proc_file(ifname, cols, count_table, subj):
    ifile = open(ifname)
    header = ifile.readline()

    col_names = header.strip().split('\t')

    for line in ifile:
        values = line.strip().split('\t')
        assert len(values) == len(col_names)

        ind = []
        subj_ind = None
        for k, sv in enumerate(values):
            name = col_names[k];
            if not cols[name]:
                i = None
            elif sv in cols[name]:
                i = cols[name].index(sv)
            else:
                i = -1
            
            if name == subj:
                subj_ind = i

            ind.append( i )
        
        for k, i in enumerate(ind):
            if i >= 0 and subj_ind >= 0:
                count_table[col_names[k]][i, subj_ind] += 1

def compute_entropy(count_table, subj, ofname):
    ofile = open(ofname, 'w')
    for name, t in count_table.iteritems():
        print 'cond_entropy( %s | %s ):\n' % (subj, name)

        supp = t.sum()
        ent = 0.0
        m, n = t.shape

        for i in range(m):
            lsum = t[i,:].sum()
            for j in range(n):
                if t[i,j]:
                    ent += t[i,j] / supp * log( lsum / t[i,j] )

        h_xy = 0.0
        for i in range(m):
            for j in range(n):
                if t[i,j]:
                    h_xy += (t[i,j] / supp) * log(supp / t[i,j])
        h_x = 0.0
        for i in range(m):
            s = t[i,:].sum()
            if s:
                h_x += (s / supp) * log(supp / s)

        h_y = 0.0
        for j in range(n):
            s = t[:,j].sum()
            if s:
                h_y += (s / supp) * log(supp / s)
        
        assert h_x <= h_xy and h_y <= h_xy,'h_x = %.3f, h_y = %.3f, h_xy = %.3f' % (h_x, h_y, h_xy)

        print '\tsupport = %d, value = %.3f\n' % (supp, ent)
        
        mic = (h_x + h_y - h_xy) / min(h_x, h_y)
        print '\tmic = %.3f\n' % mic
    
        ofile.write('%s\t%.3f\n' % (name, mic))

    ofile.close()
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'usage: <col-file> <ifile> <COL> <ofile>'
        sys.exit(1)

    cols = read_col_file(sys.argv[1])
    # print cols

    subj = sys.argv[3]
    assert subj in cols

    count_table = {}
    for c, v in cols.iteritems():
        if v is not None:
            count_table[c] = zeros((len(v), len(cols[subj])))

    ifname = sys.argv[2]
    ofname = sys.argv[4]
    proc_file(ifname, cols, count_table, subj);

    compute_entropy(count_table, subj, ofname);
