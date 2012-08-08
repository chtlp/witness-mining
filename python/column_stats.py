import sys
import glob
from collections import defaultdict

def proc_file(ifname):
    ifile = open(ifname)
    header = ifile.readline()

    col_names = header.strip().split('\t')
    col_values = [defaultdict(int) for _ in range(len(col_names))]

    for line in ifile:
        values = line.strip().split('\t')
        assert len(values) == len(col_names)

        for k, sv in enumerate(values):
            col_values[k][sv] += 1

    return col_names, col_values

def write_stat(col_names, col_values, ifname, ofile):
    ofile.write('\n#%s\n' % ifname)

    for k, name in enumerate(col_names):
        values = col_values[k].items()
        tot = sum(map(lambda (v, c): c, values))
        values = sorted(values, key=lambda (v, c): -c)

        top10_sum = sum(map(lambda (v, c): c, values[:10]))
        ofile.write('%s: ' % name)
        if top10_sum >= 0.9 * tot:
            ofile.write('\t'.join(map(lambda (v, c): v, values[:10])))
        ofile.write('\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: <ofile>'
        sys.exit(1)

    ofile = open(sys.argv[1], "w")

    for ifname in glob.glob("PERSON.TXT"):
        print 'processing %s ...\n' % ifname
        col_names, col_values = proc_file(ifname)
        write_stat(col_names, col_values, ifname, ofile)

    ofile.close()
        

    
