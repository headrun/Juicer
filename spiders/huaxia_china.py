from juicer.utils import *
from dateutil import parser

class Huaxia(JuicerSpider):
    name = 'huaxia_china'
    start_urls = ['http://www.huaxia.com/xw/dlxw/index.html','http://www.huaxia.com/xw/twxw/index.html','http://www.huaxia.com/xw/gaxw/index.html','http://www.huaxia.com/xw/gjxw/index.html','http://www.huaxia.com/xw/zhxw/index.html','http://www.huaxia.com/xw/ylxw/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//a[@class="A002"]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="Ftitle"]//text()'))
        text = textify(hdoc.select('//td[@class="px14"]//p//text()')[:-3])
        dt_added = textify(hdoc.select('//font[@color="#666666"]//text()'))
        dt_added = dt_added.split('\r')
        dt_added.pop(0)
        dt_added = ''.join(dt_added)
        dt_added = dt_added.split(u'\u51711\u9875')
        dt_added = ''.join(dt_added).strip()
        author = textify(hdoc.select('//td[@class="px14"]/p/text()')[-1])
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('url',response.url)
        yield item.process()

