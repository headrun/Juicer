from juicer.utils import *
from dateutil import parser

class StcnNews(JuicerSpider):
    name = "stcn_news"
    start_urls = ['http://company.stcn.com/cjnews/1.shtml','http://news.stcn.com/secu/','http://news.stcn.com/guonei/1.shtml','http://fund.stcn.com/','http://company.stcn.com/gsxw/1.shtml','http://company.stcn.com/cjnews/1.shtml','http://company.stcn.com/dc/1.shtml','http://company.stcn.com/qc/1.shtml','http://company.stcn.com/kj/1.shtml','http://research.stcn.com/sccl/1.shtml','http://research.stcn.com/hyyj/1.shtml','http://research.stcn.com/gsyj/1.shtml','http://research.stcn.com/hgyj/1.shtml','http://research.stcn.com/xgyj/1.shtml','http://overseas.stcn.com/news/gj/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="zz_content"]//ul[@class="mainlist"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="txt_hd"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="txt_bd lh24 fz14"]//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="txt_bd lh24 fz14"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="info"]/text()'))
        if dt_added:
            dt_added = textify(hdoc.select('//div[@class="info"]/text()')[0])
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()

