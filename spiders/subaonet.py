from juicer.utils import *
from dateutil import parser

class Subaonet(JuicerSpider):
    name = "subaonet"
    start_urls = ['http://www.subaonet.com/ori_finance/','http://www.subaonet.com/ori_travel/','http://www.subaonet.com/ori_edu/',' http://www.subaonet.com/ori_ent/','http://www.subaonet.com/ori_sports/','http://www.subaonet.com/ori_culture/','http://www.subaonet.com/ori_import/','http://www.subaonet.com/ori_livelihood/','http://www.subaonet.com/ori_society/','http://news.subaonet.com/YR_DeltaRegion/','http://news.subaonet.com/china/','http://news.subaonet.com/world/','http://news.subaonet.com/extract/','http://news.subaonet.com/military/','http://news.subaonet.com/workplace/','http://www.subaonet.com/cul/cul_news/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="bor-9fc"]//ul[@class="mode-txtlink c-lists"]//li//a//@href').extract()
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="article-content fontSizeSmall BSHARE_POP"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@class="date"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
'''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()'''

