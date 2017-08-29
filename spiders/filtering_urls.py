import sys
import csv

def main(singapore_forums_feeds_2016_10_20):
    f = open(singapore_forums_feeds_2016_10_20,'rb+')
    s = csv.reader(f)
    output_file = 'sg_forums_filter'
    for row in s:
        row = str(row).strip("[]'").strip(' ')
        if 'http' not in row:
            out_file = file(output_file,'ab+')
            out_file.write('%s\n'%row)
        else:
            print row

main('singapore_forums_feeds_2016_10_20')
