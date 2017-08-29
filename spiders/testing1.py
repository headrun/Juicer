from juicer.utils import *
from dateutil import parser
import json

class Testing(JuicerSpider):
    name = 'testing_sample'
    start_urls = 'http://www.maltatoday.com.mt/'

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        rss = hdoc.select('//div[@class="open_url"]/a/@href | //div[contains(@class,"submenu_nav_container")]//li/a/@href').extract()
        for rss2 in rss:
            if 'http' not in rss2: rss2 = 'http://www.maltatoday.com.mt' + rss2
            yield Request(rss2,self.details,response)
        #urls = hdoc.select('//ul[@class="categories-module"]/li/h4/a/@href').extract()
        #for url in urls:
            #yield Request(url,self.details,response)
        #nxt_pg = hdoc.select('//div[@class="nextPage"]/a/@href').extract()
        #if nxt_pg:yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        rss1 = textify(hdoc.select('//div[@class="icon rss"]/a/@href'))
        #for rss in rss1:
        if 'http' not in rss1: rss1 = 'http://www.maltatoday.com.mt' + rss1
        print rss1
        #link = hdoc.select('//ul[@class="categories"]/li/a/@href').extract()
        #for rss2 in link:
            #if 'http' not in rss2: rss2 = 'http://www.basearticles.com' + rss2
            #yield Request(rss2,self.details1,response)

    def details1(self,response):
        hdoc = HTML(response)
        rss = hdoc.select('//div[@class="align-right rssDiv"]/a/@href').extract()
        print 'http://www.basearticles.com'+ textify(rss)
