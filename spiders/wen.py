from juicer.utils import*
from dateutil import parser

class Wenweipo(JuicerSpider):
    name = 'wenweipo'
    start_urls = ['http://www.wenweipo.com/']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        categories = hdoc.select('//ul[@class="inline font-14"]/li/a[contains(@href,"news.wenweipo")]/@href').extract()
        for url in categories:
            url = url
            yield Request(categories,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@id="content"]//a[@class="sub_fg16 "]/@href').extract() 
        for url in links:
            url = url
            yield Request(url,self.parse_final,response)

    def parse_final(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title"]/text()'))
        text = textify(hdoc.select('//div[@id="main-content"]/p//text()'))
        date = textify(hdoc.select('//span[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//p[@class="fromInfo"]/text()'))


        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author',xcode(author)

