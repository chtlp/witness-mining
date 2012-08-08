from collections import defaultdict, OrderedDict
import csv, sqlite3, glob, sys, subprocess
from pylab import *

def analyze_columns(col_names, values):
    num = len(col_names)
    unique_values = [defaultdict(int) for _ in range(num)]

    for row in values:
        for k, c in enumerate(row):
            unique_values[k][c] += 1

    col_values = [None] * num
    for k in range(num):
        tot = sum(unique_values[k].values())
        items = sorted(unique_values[k].items(), key = lambda (v, c): -c)[:10]
        if sum(map(lambda (v, c): c, items)) >= 0.9 * tot:
            col_values[k] = map(lambda (v, c): v, items)

    return col_values


def build_count_table(col_values, col_names, values, subj):
    i = col_names.index(subj)
    assert col_values[i]

    num = len(col_values)
    count_table = [None] * num
    for k in range(num):
        if col_values[k]:
            count_table[k] = zeros((len(col_values[k]), len(col_values[i])))

    for row in values:
        u = row[i]        
        for k, v in enumerate(row):
            if col_values[k] and v in col_values[k] and u in col_values[i]:
                count_table[k][ col_values[k].index(v), col_values[i].index(u) ] += 1
    return count_table
    
def compute_entropy(count_table, col_names, subj):
    ofile = open('analyze_db.log', 'w')

    for k, t in enumerate(count_table):
        if t is None:
            continue

        print 'cond_entropy( %s | %s ):\n' % (subj, col_names[k])

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

        if not h_x:
            continue
        mic = (h_x + h_y - h_xy) / min(h_x, h_y)
        print '\tmic = %.3f\n' % mic
        ofile.write('%s\t%.3f\n' % (col_names[k], mic))
    ofile.close()

def analyze_table(col_names, values, subj):
    col_values = analyze_columns(col_names, values)
    count_table =  build_count_table(col_values, col_names, values, subj)    
    compute_entropy(count_table, col_names, subj)


def analyze_person_accident(conn, cur):
    cur.execute("PRAGMA table_info(PERSON)")
    c1 = cur.fetchall()

    cur.execute("PRAGMA table_info(ACCIDENT)")
    c2 = cur.fetchall()

    cur.execute('select * from PERSON JOIN ACCIDENT where PERSON.CASENUM == ACCIDENT.CASENUM')
    res = cur.fetchall()

    cols = map(lambda t: t[1], c1) + map(lambda t: t[1], c2)
    analyze_table(cols, res, 'INJ_SEV')

if __name__ == '__main__':
    conn = sqlite3.connect('traffic.db')
    conn.text_factory = str

    cur = conn.cursor()

    analyze_person_accident(conn, cur)
    
    cur.close()
    conn.close()
