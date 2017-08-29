from juicer.utils import *
from dateutil import parser

class NewsIndiaOnline(JuicerSpider):
    name = "newsindiaonline"
    start_urls = ['http://news.indiaonline.in/Politics/', 'http://news.indiaonline.in/Entertainment/', 'http://news.indiaonline.in/Business-Economy/', 'http://news.indiaonline.in/Sports/', 'http://news.indiaonline.in/Crime/', 'http://news.indiaonline.in/International/', 'http://news.indiaonline.in/Health/', 'http://news.indiaonline.in/Science/', 'http://news.indiaonline.in/Weather/', 'http://news.indiaonline.in/Religion/']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="ht-nws"]/a/@href | //div[@class="cont"]/a/@href')
        for url in urls:
            url = 'http://news.indiaonline.in/SC-defers-hearing-on-bail-to-Shahabuddin-to-Wednesday-1444835'
            yield Request(url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//div[@class="hed"]//h1/text()'))
        text = textify(hdoc.select('//div[@class="nd"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="tl"]//h3/text()')).lower()
       #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)


        '''item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('url', response.url)

        yield item.process()'''
