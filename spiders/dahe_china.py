from juicer.utils import *
from dateutil import parser

class Dahe(JuicerSpider):
    name = "dahe_china"
    start_urls = ['http://news.dahe.cn/sz/','http://news.dahe.cn/city_zz/index.html','http://news.dahe.cn/csxw/','http://news.dahe.cn/tyxw/','http://news.dahe.cn/100871008/index.html','http://news.dahe.cn/100871037/index.html','http://news.dahe.cn/100871050/index.html','http://news.dahe.cn/100871054/index.html','http://ent.dahe.cn/bfy/','http://ent.dahe.cn/bg/','http://ent.dahe.cn/mxbgt/','http://ent.dahe.cn/bggzd/','http://news.dahe.cn/gnxw/','http://news.dahe.cn/gjxw/','http://news.dahe.cn/hyzx/','http://news.dahe.cn/100871263/index.html','http://news.dahe.cn/sh/','http://news.dahe.cn/100871271/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="main"]//div[@class="dConL"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@id="mainCon"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//div[@id="conInfo"]//text()')[1])
        import pdb;pdb.set_trace()
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        if not author:
            author = textify(hdoc.select('//div[@id="conInfo"]//text()')[3])
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

