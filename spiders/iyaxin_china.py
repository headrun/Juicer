from juicer.utils import *
from dateutil import parser

class Iyaxin(JuicerSpider):
    name = "iyaxin_china"
    start_urls = ['http://news.iyaxin.com/node_88760.htm','http://news.iyaxin.com/node_58237.htm','http://news.iyaxin.com/node_55909.htm','http://news.iyaxin.com/node_55908.htm','http://news.iyaxin.com/node_55907.htm','http://news.iyaxin.com/node_88759.htm','http://news.iyaxin.com/node_55865.htm','http://ent.iyaxin.com/node_3559.htm','http://ent.iyaxin.com/node_3560.htm','http://ent.iyaxin.com/node_15817.htm','http://ent.iyaxin.com/node_15818.htm','http://ent.iyaxin.com/node_40837.htm','http://ent.iyaxin.com/node_15839.htm','http://ent.iyaxin.com/node_15837.htm','http://news.iyaxin.com/node_101437.htm','http://news.iyaxin.com/node_101437.htm','http://news.iyaxin.com/node_55879.htm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul[@class="text-list-ul"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="content"]/p/text()')[:-1])
        if not text:
            text = textify(hdoc.select('//div[@class="article-detail"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="article-detail"]//div[style="TEXT-ALIGN: left"]//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        author = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        if author:
            author = author.split(u'\uff1a')[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()
