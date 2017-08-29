from juicer.utils import *
from dateutil import parser

class Testing(JuicerSpider):
    name = 'testing_sample'
    start_urls = 'http://www.amazon.co.jp/gp/search/ref=sr_gnr_fkmr0?rh=i%3Aaps%2Ck%3A%EF%BD%B1%EF%BE%98%EF%BD%B4%EF%BD%B0%EF%BE%99%EF%BD%B2%EF%BD%B5%EF%BE%9D%EF%BE%8A%EF%BE%9F%EF%BE%9C%EF%BD%B0%EF%BD%BC%EF%BE%9E%EF%BD%AA%EF%BE%99%EF%BD%BB%EF%BD%B2%EF%BD%B4%EF%BE%9D%EF%BD%BD%EF%BE%8C%EF%BE%9F%EF%BE%97%EF%BD%BD+%E3%81%A4%E3%82%81%E3%81%8B%E3%81%88&keywords=%EF%BD%B1%EF%BE%98%EF%BD%B4%EF%BD%B0%EF%BE%99%EF%BD%B2%EF%BD%B5%EF%BE%9D%EF%BE%8A%EF%BE%9F%EF%BE%9C%EF%BD%B0%EF%BD%BC%EF%BE%9E%EF%BD%AA%EF%BE%99%EF%BD%BB%EF%BD%B2%EF%BD%B4%EF%BE%9D%EF%BD%BD%EF%BE%8C%EF%BE%9F%EF%BE%97%EF%BD%BD+%E3%81%A4%E3%82%81%E3%81%8B%E3%81%88&ie=UTF8&qid=1457350167'
    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        rss = hdoc.select('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()
        
        for rss2 in rss:
            print rss2
            #yield Request(rss2,self.details,response)
        #urls = hdoc.select('//ul[@class="categories-module"]/li/h4/a/@href').extract()
        #for url in urls:
            #yield Request(url,self.details,response)
        nxt_pg = hdoc.select('//div[@class="nextPage"]/a/@href').extract()
        if nxt_pg:yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        rss1 = textify(hdoc.select('//link[@type="application/rss+xml"]/@href'))
        #for rss in rss1:
        if 'http' not in rss1: rss1 = 'http://www.siliconinvestor.com/' + rss1
        print rss1
        #link = hdoc.select('//ul[@class="categories"]/li/a/@href').extract()
        #for rss2 in link:
            #if 'http' not in rss2: rss2 = 'http://www.basearticles.com' + rss2
            #yield Request(rss2,self.details1,response)

    def details1(self,response):
        hdoc = HTML(response)
        rss = hdoc.select('//div[@class="align-right rssDiv"]/a/@href').extract()
        print 'http://www.basearticles.com'+ textify(rss)
