from juicer.utils import*
from dateutil import parser

class PissedConsumer(JuicerSpider):
    name = 'pissed_consumer'
    start_urls = ['https://www.pissedconsumer.com/browse-reviews.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//h2[@itemprop="name"]//a/@href').extract()
        for url in urls:
            if 'http' not in url:
                url = 'https://www.pissedconsumer.com' + url
            yield Request(url,self.parse_details,response)

        next_page = textify(hdoc.select('//div[@class="pagination-new"]//li[contains(@class,"next")]/a/@href'))
        if next_page:
            if 'http' not in next_page:
                next_page = 'https://www.pissedconsumer.com' + next_page
            yield Request(next_page,self.parse,response)

    def parse(self,response):
        hdoc= HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]/text()'))
        text = textify(hdoc.select('//div[@itemprop="reviewBody"]/p/text()'))
