from juicer.utils import*
from dateutil import parser
import codecs
import csv
import xlwt


class Complaintsboard(JuicerSpider):
    name = 'complaint_board'
    start_urls = ['http://www.complaintsboard.com/']
    row_num = 0
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="item-row complaint"]/h4/a/@href').extract()
        for url in urls[0:5]:
            if 'http' not in url:
                url = 'http://www.complaintsboard.com/' +url

            yield Request(url ,self.parse_details,response)
        '''
        next_page = textify(hdoc.select('//nav[@class="pages"]/a[contains(text(),"Next")]/@href'))
        if next_page:
            if 'http:' not in next_page:
                next_page = 'http://www.complaintsboard.com'+next_page
            yield Request(next_page,self.parse,response)
        '''

    def parse_details(self,response):
        hdoc = HTML(response)
        data_list = []
        person_against = textify(hdoc.select('//td[@class="complaint"]//text()'))
        complaint_title = textify(hdoc.select('//td[@class="compl-text"]//h1/text()'))
        complaint_desc = textify(hdoc.select('//div[@itemprop="reviewBody"]//text()'))
        author_name = textify(hdoc.select('//span[@itemprop="givenName"]/text()'))
        date = textify(hdoc.select('//span[@itemprop="dateCreated"]/text()'))
        country = textify(hdoc.select('//span[@itemprop="addressCountry"]/text()'))
        category = textify(hdoc.select('//td/span/a[contains(@href,"category")]/text()'))
        data_list = "#<>#".join([response.url,person_against,complaint_title,complaint_desc,author_name,date,country,category])
        row_num = self.row_num 
        self.sheet1.write(row_num, 0, data_list)
        self.row_num= self.row_num+1
        self.book.save("newcomplaintsboard.xls")
        '''
        print person_against + '<<>>' + complaint_title + '<<>>' + complaint_desc + '<<>>' + author_name + '<<>>' + date + '<<>>' + country + '<<>>' + category
        print '/n'
        print '/n'
        print response.url
        print 'person_against:',xcode(person_against)
        print 'complaint_title:',xcode(complaint_title)
        print 'complaint_desc:',xcode(complaint_desc)
        print 'author_name:',xcode(author_name)
        print 'date:',xcode(date)
        print 'country:',country
        print 'category:',category
        '''
