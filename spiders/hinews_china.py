from juicer.utils import *
from dateutil import parser

class Hinews(JuicerSpider):
    name = "hinews_china"
    start_urls = ['http://www.hinews.cn/news/newsmore.shtml']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="fl f14"]//a[@class="cBlue6"]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="f20 fb fc cBlue_d4"]//text()'))
        if not title:
            title = textify(hdoc.select('//div[@class="l46 vm bg3_p"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="BSHARE_POP"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//span[@class="fl"]/text()'))
        dt_added = dt_added.split(u'\uff1a')
        dt_added.pop(0)
        dt_added =  ' '.join(dt_added)
        author = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        if not author:
            author = textify(hdoc.select('//div[@class="vm"]/text()')[-2:])
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ' '.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

