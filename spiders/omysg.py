from juicer.utils import *
import datetime
from datetime import timedelta
from dateutil import parser
import ast
import time

class OmySiteSGNEW(JuicerSpider):
    name = "omy_sg"
    start_urls = "http://www.omy.sg/"
    allow_domian = ['http://showbiz.omy.sg/', 'http://lifestyle.omy.sg/', 'http://news.omy.sg/', 'http://yzone.omy.sg/']


    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//ul[@id="nav"]/li//ul/li/a/@href')
        for url in nodes:
            yield Request(url, self.parse_next, response)

    def parse_next(self,response):
        hdoc = HTML(response)
        table1 = hdoc.select('//detail/ul/li')
        for tab in table1:
           terminal_link = textify(tab,select('.//a[@class="title"]/@href'))
           yield Request(terminal_link, self.parse_terminal)

        nxt_page = textify(hdoc.select('//li/a[contains(text(),"next")]/@href'))
        if nxt_page:
           yield Request(nxt_page, self.parse_next, response)

    def parse_terminal(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="storytitle"]/text()'))
        date = hdoc.select('//detail[@class="publication"]//span[@class="stamp"]/text()').extract()[0].replace('on','').replace("\t",'').strip()
        dt_added = parse_date(xcode(date)) - datetime.timedelta(hours=9)
        dt_final = dt_added.strftime('%Y-%m-%d %H:%M:%S')

        author = textify(hdoc.select('//span[@class="contributor"]/a/text()').extract())
        text =  textify(hdoc.select('//detail[@class="storybox"]/p/text()').extract())

        print 'url', response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'author', xcode(author)
        print 'date', xcode(dt_final)

