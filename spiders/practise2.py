from juicer.utils import*
from dateutil import parser

class Practise(JuicerSpider):
    name = 'practise2'
    start_urls= ['http://absoluteindianews.com/hindi/?cat=32']
    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//li[contains(@id, "menu-item")]/a/@href').extract()
        for link in links:
            if 'http' not in link: lin='http://www.philippinenews.com' + link
            yield Request(link,self.parse,response)

        rss_link = hdoc.select('//link[contains(@type, "application")]/@href').extract()[2]
        if 'http' not in rss_link:
            rss_link =  'http://www.philippinenews.com' + rss_link
        #rss_link = hdoc.select('//a[@class="rss"]/@href').extract()
        f = open("rss_link_feed", "a")
        f.write(rss_link)
        f.write("\n")
        
        print rss_link


