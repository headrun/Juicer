from juicer.utils import *
from dateutil import parser

class Hangzhou(JuicerSpider):
    name = 'hangzhou_china'
    start_urls = ['http://news.hangzhou.com.cn/gjxw/index.htm','http://news.hangzhou.com.cn/gnxw/index.htm','http://news.hangzhou.com.cn/gnxw/index.htm','http://news.hangzhou.com.cn/xwzxhz/index.htm','http://news.hangzhou.com.cn/zjnews/index.htm','http://news.hangzhou.com.cn/jjxw/index.htm','http://news.hangzhou.com.cn/shxw/index.htm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//a[@class="ge_01color11" ]//@href')
        if not urls:
            urls = hdoc.select('//td//a[@class="le_st14black"]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td[@class="xwzx_wname01"]//text()'))
        text = textify(hdoc.select('//td[@class="xwzx_wname02"]//p//text()'))
        author = textify(hdoc.select('//td[@align="right"]//text()')[-1])
        author = author.split(u'\xa0\xa0\xa0\xa0')
        author.pop(1)
        author = ' '.join(author)
        author = author.split(u'\uff1a')
        if author[1] is u'\u8d23\u4efb\u7f16\u8f91':
            author = author[2]
        else:
            author = author[1]
        dt_added = textify(hdoc.select('//td[@align="center"]/text()')[9])
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('url',response.url)

