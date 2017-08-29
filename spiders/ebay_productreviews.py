from juicer.utils import *
from dateutil import parser

class EbayProductreviews(JuicerSpider):
    name  = 'ebay_productreviews'
    start_urls = ['http://www.ebay.in/rpp/deals/electronics/electronics/laptops/','http://www.ebay.in/sch/Clothing-Accessories-/11450/i.html']

    def parse(self,response):
        hdoc = HTML(response)
        product_links = hdoc.select('//a[@class="ranc"]/@href').extract() or hdoc.select('//a[@class="vip"]/@href').extract()

        for product_link in product_links:
            yield Request(product_link,self.parse_next,response)

        next_page = textify(hdoc.select('//a[@class="gspr next"]/@href'))
        if next_page:
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)

