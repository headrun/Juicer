from juicer.utils import *
from dateutil import parser

class China_21cbh(JuicerSpider):
    name = '21cbh_china'
    start_urls = ['http://www.21cbh.com/channel/yaowen/','http://money.21cbh.com/cjyw/','http://money.21cbh.com/hk/','http://money.21cbh.com/america/','http://money.21cbh.com/IPO_Express/','http://jingji.21cbh.com/ggsj/','http://jingji.21cbh.com/zgjj/','http://jingji.21cbh.com/ggsj/','http://jingji.21cbh.com/newsmaker/','http://ent.21cbh.com/sports/','http://ent.21cbh.com/classic/','http://fangchan.21cbh.com/fangshi/','http://auto.21cbh.com/qiche-chejiepinglun/','http://auto.21cbh.com/hangyexinwen/qiche-qicheyaowen/','http://auto.21cbh.com/qiche-qicheshenghuo/','http://auto.21cbh.com/qiche-gundong/','http://auto.21cbh.com/lishi/','http://www.21cbh.com/channel/yuanchuang/','http://www.21cbh.com/channel/zhuanti/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="piece3"]//a[@class="titles"]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//span[@class="the_title"]//text()'))
        text = textify(hdoc.select('//div[@class="article_content"]//p/text()'))
        if not text:
             text = textify(hdoc.select('//div[@class="article_content"]/text()'))
        dt_added = textify(hdoc.select('//span[@class="the_title2"]/text()')[1:])
        if not dt_added:
            dt_added = textify(hdoc.select('//span[@class="the_title2"]/text()'))
            dt_added = dt_added.split('\t')
            dt_added.pop(0)
            dt_added =' '.join(dt_added)
        dt_added = dt_added.strip()
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//span[@class="fccc"]//text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        author = author.split(u'\uff09')
        author = author[0]

        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('url',response.url)
        yield item.process()
