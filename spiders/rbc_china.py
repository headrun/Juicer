from juicer.utils import *
from dateutil import parser

class RbcChina(JuicerSpider):
    name = 'rbc_china'
    start_urls = ['http://www.rbc.cn/yw/','http://ent.rbc.cn/djbd/index.htm','http://health.rbc.cn/jkzx/index.htm','http://www.rbc.cn/jdxw/index.htm','http://jymdm.rbc.cn/jymdm/zjjyrd/index.htm','http://gongyi.rbc.cn/wndll/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul[@class="list"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="art_contnet"]//p//text()'))
        dt_added = textify(hdoc.select('//p[@class="t_info"]//text()')[2])
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()

