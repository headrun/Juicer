from juicer.utils import *
from dateutil import parser

class Practise(JuicerSpider):
    name = 'practise1'
    start_urls = ['http://eunited.com.my/category/news/%E5%8C%97%E7%A0%82%E6%96%B0%E9%97%BB/']

    def parse(self,response):
        hdoc = HTML(response)
        category_links = hdoc.select('//id[contains(@id, "menu-item")]/a/@href').extract()
        for link in category_links:
            #link = ''.join(link.split('./'))
            yield Request(link, self.parse,response)
        rss_link = hdoc.select('//link[contains(@type, "application")]/@href').extract()[2]
        #rss_link = textify(hdoc.select('//a[@class="Rss mini"]/@href'))]
        f = open("rss_links.text", "a")
        f.write(rss_link)
        f.write("\n")

        print rss_link    
