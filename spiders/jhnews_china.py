from juicer.utils import *
from dateutil import parser

class Jhnews(JuicerSpider):
    name = "jhnews_china"
    start_urls = ['http://www.jhnews.com.cn/news/realtimenews/','http://www.jhnews.com.cn/news/headlines/','http://www.jhnews.com.cn/news/todaynews/','http://www.jhnews.com.cn/news/jinhuanews/','http://www.jhnews.com.cn/news/china/','http://www.jhnews.com.cn/news/world/','http://www.jhnews.com.cn/news/review/','http://www.jhnews.com.cn/news/ent/','http://w3.jhnews.com.cn/news/cjpd/','http://www.jhnews.com.cn/news/dznews/xjabdzj/','http://www.jhnews.com.cn/news/dznews/dz/','http://www.jhnews.com.cn/news/dznews/jmbdzj/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="p_left"]//div[@class="c_tit"]//h1//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="article-content fontSizeBig BSHARE_POP"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//header[@class="picture-header"]//p[@class="summary"]//text()'))
        dt_added = textify(hdoc.select('//span[@class="post-time"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//div[@class="article-infos"]//span[@class="date"]//text()')[0])
        author = textify(hdoc.select('//div[@class="editor"]//span//text()')[0])
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
