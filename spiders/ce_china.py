from juicer.utils import *
import re

class CeChina(JuicerSpider):
    name = "ce_china"
    start_urls = ['http://wap.ce.cn/yw/','http://wap.ce.cn/cy/','http://wap.ce.cn/szsh/','http://wap.ce.cn/intl/','http://wap.ce.cn/stock/','http://wap.ce.cn/money/','http://wap.ce.cn/sp/','http://wap.ce.cn/auto/','http://wap.ce.cn/fc/','http://wap.ce.cn/culture/','http://wap.ce.cn/fashion/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="newsbox"]//ul[@id="newslist"]//li//a//@href')
        for url in urls:
            url = textify(url)
            final_url = re.search(r'^./[0-9]',url)
            if final_url:
                yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="title"]//text()'))
        text = textify(hdoc.select('//div[@id="content"]//div[@class="TRS_Editor"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="info"]//text()')[1])
        author = textify(hdoc.select('//div[@id="newsbox"]/p/text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author = author[0].replace(u'\uff09', '')
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))


        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()
