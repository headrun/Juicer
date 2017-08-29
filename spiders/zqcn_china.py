from juicer.utils import *
from dateutil import parser

class Zqcn(JuicerSpider):
    name = "zqcn_china"
    start_urls = ['http://qiye.zqcn.com.cn/gzywlb/','http://trade.zqcn.com.cn/cul/','http://trade.zqcn.com.cn/travel/','http://trade.zqcn.com.cn/food/','http://trade.zqcn.com.cn/finance/','http://trade.zqcn.com.cn/realty/','http://trade.zqcn.com.cn/energy/','http://trade.zqcn.com.cn/auto/','http://trade.zqcn.com.cn/ce/','http://news.zqcn.com.cn/qyjj/','http://news.zqcn.com.cn/szyw/','http://news.zqcn.com.cn/hqcj/','http://news.zqcn.com.cn/zdsj/','http://qiye.zqcn.com.cn/qyxw/','http://news.zqcn.com.cn/zqsp/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="lf660"]//ul[@class="newslist"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//div[@class="headline"]//h2//text()'))
        text = textify(hdoc.select('//div[@class="article_txt"]//text()'))
        date_author = textify(hdoc.select('//div[@class="headline"]/span/text()')[0])
        date_author = date_author.split(u'\xa0\xa0')
        dt_added = date_author[0]
        author = date_author[1].split(u'\uff1a')
        author = author[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

