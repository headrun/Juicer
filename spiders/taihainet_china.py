from  juicer.utils import *
from dateutil import parser

class Taihainet(JuicerSpider):
    name = 'taihainet_china'
    start_urls = ['http://www.taihainet.com/news/twnews/twmzmj/','http://www.taihainet.com/news/twnews/twrw/','http://www.taihainet.com/news/txnews/cnnews/sh/','http://www.taihainet.com/news/txnews/sz/','http://www.taihainet.com/news/military/zgjq/','http://www.taihainet.com/news/military/lbsm/','http://www.taihainet.com/news/military/hqjs/','http://www.taihainet.com/news/pastime/bagua/','http://www.taihainet.com/news/pastime/sports/','http://www.taihainet.com/news/pastime/yllq/','http://www.taihainet.com/lifeid/science/','http://www.taihainet.com/lifeid/culture/whdht/','http://www.taihainet.com/lifeid/culture/zsfz/','http://www.taihainet.com/lifeid/culture/dwys/','http://www.taihainet.com/lifeid/culture/lshc/','http://www.taihainet.com/news/shequxm/cyq/Index.html','http://www.taihainet.com/news/shequxm/hwq/Index.html','http://www.taihainet.com/news/shequxm/lmq/Index.html','http://www.taihainet.com/news/shequxm/pjh/Index.html','http://www.taihainet.com/news/shequxm/myq/Index.html','http://www.taihainet.com/news/shequxm/myq/Index.html','http://www.taihainet.com/news/shequxm/xjzq/Index.html','http://www.taihainet.com/news/shequxm/jsq/Index.html','http://www.taihainet.com/news/shequxm/qyq/Index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="A_L_con"]//p//a//@href').extract()
        for url in urls:
            yield Request(url,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="page-box clear ov"]//li//a[@class="next"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[contains(@class, "article")]//p//text()'))
        date = textify(hdoc.select('//div[@class="page-info wrapper ovv"]//time//text()')) or textify(hdoc.select('//div[@class="page-info"]//span[2]//text()')) or textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

     
        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()
