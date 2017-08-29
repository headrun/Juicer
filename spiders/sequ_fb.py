import sys
import csv
import os 
def main(seq_fb):
    f = open(seq_fb,'rb+')
    seq = csv.reader(f)
    output_file = file("seq_ids", "w+")
    output_file1 = file("seq_urls","w+")

    #output_file = 'seq_ids'
    #output_file1 = 'seq_urls'

    for row in seq:
        row = str(row).encode("utf8")
        row1 = str(row).strip("[]'").strip(' ').split('&id=')[-1]

        if '&comment' not in row1:
            #out_file = file(output_file,'ab+')
            output_file.write('https://www.facebook.com/feeds/page.php?id=%s&format=rss20,%s\n'%(row1,row1))
        else:
            row1 = row1.split('&')[0]
            #out_file1 = file(output_file1,'ab+')
            output_file1.write('%s,%s\n'%(str(row).strip("[]'").strip(),row1))

main('seq_fb')
