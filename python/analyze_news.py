from collections import defaultdict, OrderedDict
import sqlite3, glob, sys, subprocess, codecs
from datetime import date

sys.path.append('/home/tlp/Programs/python-lib')
import ucsv as csv

def str2date(s):
    s = s.replace('\t','').replace('/','-') 
    try:
        t = tuple(map(int, s.split('-')))
        return date(*t)
    except:
        print s
        sys.exit(1)

def load_ShuiNi():
    intervals = []
    with open('shui_ni.txt') as f:
        for line in f:
            if not line.strip():
                continue
            d1, d2 = line.strip().split()
            d1, d2 = map(str2date, (d1, d2))
            intervals.append( (d1, d2) )
    return intervals

def ShuiNi_days(intervals):
    n = 0
    for s, t in intervals:
        n += (t-s).days + 1
    return n

def lies_in(d, intervals):
    for s, t in intervals:
        if d >= s and d <= t:
            return True
    return False

def analyze_ShuiNi(shui_ni_dates):
    shui_ni_cc = 0
    tot = 0

    st_date = date(3000, 1, 1)
    end_date = date(1, 1, 1)

    corrupted = 0

    for fname in glob.glob('news-data/Detail/*.utf8.csv'):
        print fname
        with open(fname) as ifile:

            for line in ifile:
                # cope with corrupted lines
                if line.find(',') == -1:
                    corrupted += 1
                    continue

                try:
                    d = str2date(line.split(',')[2].strip())
                except Exception as e:
                    print repr(line)
                    raise e

                tot += 1
                if lies_in(d, shui_ni_dates):
                    shui_ni_cc += 1

                st_date = min(st_date, d)
                end_date = max(end_date, d)

    print 'corrupted %d\n' % corrupted
    print st_date, end_date

    sd = ShuiNi_days(shui_ni_dates)
    td = (end_date - st_date).days + 1
    print '%d / %d = %.3f' % (shui_ni_cc, sd, (shui_ni_cc+0.0) / sd)
    print '%d / %d = %.3f' % (tot, td, (tot+0.0) / td)
            

if __name__ == '__main__':
    intervals = load_ShuiNi()

    analyze_ShuiNi(intervals)
