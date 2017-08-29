from juicer.utils import *
from dateutil import parser

class XcfChina(JuicerSpider):
    name = 'xcf_china'
    start_urls = ['http://www.xcf.cn/jrdd/','http://www.xcf.cn/kuaixun/hgzx/','http://www.xcf.cn/kuaixun/glsc/','http://www.xcf.cn/kuaixun/gscy/','http://www.xcf.cn/kuaixun/jqzh/','http://www.xcf.cn/kuaixun/mosc/','http://www.xcf.cn/kuaixun/ggyt/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="columns_content2"]//h1//a//@href')
        if not urls:
            urls = hdoc.select('//div[@class="luxury_news9_list"]//ul//li//p//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="body_content_txt"]//p//text()'))
        if not text:
             text = textify(hdoc.select('//div[@class="body_content_txt"]//text()'))
        dt_added = textify(hdoc.select('//div[@class="body_content_detail2"]//ul/li/text()')[1])
        author = textify(hdoc.select('//div[@class="body_content_detail2"]//ul/li/text()')[2])
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()


