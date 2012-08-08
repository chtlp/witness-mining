import sys, glob
import codecs
def convert_file(ifname, ofname):
    with open(ifname) as ifile, codecs.open(ofname, 'w', 'utf-8') as ofile:
        l = ifile.read()
        u = unicode(l, 'gb2312', 'ignore')
        ofile.write(u)
    
if __name__ == '__main__':
    ofile = open('tmp.txt', 'w')
    for fname in glob.glob('news-data/Detail/*.csv'):
        if fname.endswith('.utf8.csv'):
            continue
        ofname = fname[:-4] + '.utf8.csv'
        
        print fname, ofname

        convert_file(fname, ofname)



    
