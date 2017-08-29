import sys
import csv

def main(taiwan_news_feeds_2016_02_25 ):
    f = open('taiwan_news_feeds_2016_02_25','r')
    s = csv.reader(f)
    output_file = 'tw_new_alexalinks'
    for i in s:
        i = str(i).strip("'[]")
        out_file = file(output_file,'ab+')
        out_file.write('http://www.alexa.com/siteinfo/http://%s\n'%i)
        out_file.close()

main('taiwan_news_feeds_2016_02_25 ')
