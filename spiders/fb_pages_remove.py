from juicer.utils import *
from lsapi import lsapi
import feedparser
import urlparse
import urllib2
import hashlib
import sys, time

l = lsapi('member-30eede4fd6', '3f741ad5c9e73ee3ea74a6b1c1b6e36d')

categories = ['news', 'blogs', 'forums', 'networks']

def main(fname):

    db, db_name = get_cursor()
    i_file = open(fname, 'r').readlines()
    count = 0

    urls_exist = open('urls_exist_24_01_2015', 'a')

    for f in i_file:
        count += 1
        page_id = f.strip().split('/')[-1]
        import pdb;pdb.set_trace()
    	try:
            db.remove(db_name, "fbpages", spec={'page_id':page_id})
            print 'Deleted :',f
    	except Exception as e: print 'exception in updating feeds into Index ::', e


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
