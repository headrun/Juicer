from juicer.utils import *
from dateutil import parser

class AbpIndia(JuicerSpider):
    name = 'abp_india'
    start_urls = ['http://www.abplive.in/']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        categories = hdoc.select('//li[contains(@id,"menu-item")]/a[contains(@href,"http")]/@href').extract()
        for category in categories:
            yield Request(category,self.parse_links,response)

    def parse(self,response):
        hdoc = HTML(response)
        links = textify(hdoc.select('//div[@class="col-sm-9"]//a/@href'))
        for link in links:
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="arH"]/text()'))
        text = textify(hdoc.select('//div[@id="_content"]//p/text()'))
        date = textify(hdoc.select('//div[@class="col-sm-12 _src"]/span/text()')).split('|')[0]
        author = textify(hdoc.select('//div[@class="col-sm-12 _src"]/span/text()')).split('|')[1]


        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'date',xcode(date)
        print 'author',xcode(author)

