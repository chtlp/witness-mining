import sys
from collections import defaultdict

if __name__ == '__main__':
    ifname = sys.argv[1]
    ofname = sys.argv[2]
    print 'STAT %s\n' % ifname

    ifile = open(ifname)
    header = ifile.readline()

    col_names = header.strip().split('\t')
    col_values = [defaultdict(int) for _ in range(len(col_names))]

    for line in ifile:
        values = line.strip().split('\t')
        assert len(values) == len(col_names)

        for k, sv in enumerate(values):
            col_values[k][sv] += 1


    ofile = open(ofname, "w")
    for name in col_names:
        ofile.write('%s\n' % name)
    ofile.write('\n')

    for k, name in enumerate(col_names):
        values = col_values[k].items()
        tot = sum(map(lambda (v, c): c, values))
        values = sorted(values, key=lambda (v, c): -c)

        ofile.write('%s, total=%d, unique=%d\n' % (name, tot, len(values)))

        for (v, c) in values[:10]:
            ofile.write('\t%s: %.3f\n' % (v, (c+0.0) / tot))

        ofile.write('\n')

    ofile.close()
        

    
