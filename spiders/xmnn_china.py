from juicer.utils import *
from dateutil import parser

class Xmnn(JuicerSpider):
    name = "xmnn_china"
    start_urls = ['http://news.xmnn.cn/a/xmxw/shbt/','http://news.xmnn.cn/a/hxxw/syxx/','http://news.xmnn.cn/a/hxxw/lyzx/','http://news.xmnn.cn/a/hxxw/gsxw/zbcs','http://news.xmnn.cn/a/hxxw/gsxw/zbcs','http://news.xmnn.cn/a/hxxw/mtwl/','http://news.xmnn.cn/a/hxxw/whty/','http://news.xmnn.cn/a/hxxw/zwms/','http://news.xmnn.cn/a/hxxw/cjxf','http://news.xmnn.cn/a/hxxw/shfz','http://news.xmnn.cn/a/hxxw/syxx','http://news.xmnn.cn/a/wybb/','http://news.xmnn.cn/a/thxw/','http://news.xmnn.cn/a/gnxw/','http://news.xmnn.cn/a/gjxw/','http://news.xmnn.cn/a/shxw/','http://news.xmnn.cn/a/jjxw/','http://news.xmnn.cn/a/ylxw/','http://news.xmnn.cn/a/xmxw/bxms/','http://news.xmnn.cn/a/xmxw/wybb','http://news.xmnn.cn/a/xmxw/jrtx/','http://news.xmnn.cn/a/xmxw/jjxf/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list active"]//ul//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="b"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="m m39"]//div[@class="b"]//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//span[@class="s1"]//text()'))
            (extra_data,dt_added,time) = dt_added.split(' ')
            dt_added = dt_added + " " + time
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        if not author:
            author = textify(hdoc.select('//div[@class="fr2"]/text()'))
            author = author.split(u'\uff1a')
            author = author[1]
            (author,extra_data) = author.split(u'\u6765\u6e90')
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

