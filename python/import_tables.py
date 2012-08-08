from collections import defaultdict, OrderedDict
import csv, sqlite3, glob, sys, subprocess

indexed_cols = set(['CASENUM'])

def import_table(cur, ifname):
    t_name = ifname.split('.')[0]
    cur.execute('DROP TABLE IF EXISTS %s' % t_name)

    cols = analyze_table(ifname)
    col_desc = ', '.join(map(lambda (n, t): '%s %s' % (n, t), cols.items()))
    cur.execute('CREATE TABLE %s (%s)' % (t_name, col_desc))

    ic = ', '.join(indexed_cols.intersection(cols.keys()))
    print ic
    cur.execute('CREATE INDEX %s_INDEX ON %s (%s)' % (t_name, t_name, ic))
    
    with open(ifname) as ifile:
        dr = csv.reader(ifile, delimiter='\t')        
        to_db = map(tuple, dr)[1:]
    
    col_names = ', '.join(cols.keys())
    col_quest = ', '.join(map(lambda n: '?', cols.keys()))
    cur.executemany('INSERT INTO %s (%s) VALUES (%s)' % (t_name, col_names, col_quest), to_db)
    # cur.execute('INSERT INTO %s (%s) VALUES (%s)' % (t_name, col_names, col_quest), to_db[0])
    print cur.rowcount
    
def analyze_table(ifname):
    ifile = open(ifname)
    cols = ifile.readline()
    cols = cols.strip().split('\t')

    col_int = defaultdict(lambda: None)
    col_float = defaultdict(lambda: None)
    col_str = defaultdict(lambda: None)

    for line in ifile:
        values = line.strip().split('\t')
        assert len(values) == len(cols)

        for n, v in zip(cols, values):
            if col_int[n] is not False:
                try:
                    vint = int(v)
                except:
                    col_int[n] = False
                else:
                    if abs(vint) < 10000:
                        col_int[n] = True
                    else:
                        col_int[n] = col_float[n] = False

            if col_float[n] is not False:
                try:
                    vfloat = float(v)
                except:
                    col_float[n] = False
                else:
                    col_float[n] = True
                
    col_types = OrderedDict()
    for n in cols:
        if col_int[n]:
            col_types[n] = 'INTEGER'
        elif col_float[n]:
            col_types[n] = 'REAL'
        else:
            col_types[n] = 'TEXT'
    return col_types

if __name__ == '__main__':
    conn = sqlite3.connect('traffic.db')
    conn.text_factory = str

    cur = conn.cursor()

    for fname in glob.glob('*.TXT'):
        print fname
        import_table(cur, fname)
        conn.commit()

    cur.close()
    conn.close()
