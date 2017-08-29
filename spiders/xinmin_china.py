from juicer.utils import *
from dateutil import parser

class Xinmin(JuicerSpider):
    name = "xinmin_china"
    start_urls = ['http://shanghai.xinmin.cn/tfbd/','http://shanghai.xinmin.cn/tt/','http://shanghai.xinmin.cn/xmsq/','http://shanghai.xinmin.cn/msrx/','http://shanghai.xinmin.cn/xmsz/','http://news.xinmin.cn/domestic/rollnews/','http://news.xinmin.cn/world/rollnews/','http://biz.xinmin.cn/lb.html','http://sports.xinmin.cn/lb.html','http://ent.xinmin.cn/lb.html','http://tech.xinmin.cn/lb.html','http://health.xinmin.cn/jkys/','http://op.xinmin.cn/chwl/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="MP_listpagelist"]//ul[@class="nodelist"]//li//h2//a//@href')
        for url in urls:
            import pdb;pdb.set_trace()
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="MP_article"]/p//text()'))
        dt_added = textify(hdoc.select('//div[@class="MP_datetime"]//text()'))
        author = textify(hdoc.select('//div[@class="MP_editor"]//text()'))
        if author:
            author = author.split(u'\uff1a')
            author = author[1]
            author = author.split(u'\uff09')
            author = author[0]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
"""
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
 #       yield item.process()
#"""
