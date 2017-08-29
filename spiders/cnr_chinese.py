from juicer.utils import *
from dateutil import parser

class CnrCn(JuicerSpider):
    name = "cnr_china"
    start_urls = ['http://news.cnr.cn/gjxw/gnews/','http://news.cnr.cn/native/gd/','http://news.cnr.cn/native/wx/shxw/','http://finance.cnr.cn/1/yw/','http://finance.cnr.cn/1/yw/','http://tech.cnr.cn/techds/','http://tech.cnr.cn/techit/','http://tech.cnr.cn/techhlw/','http://tech.cnr.cn/techyd/','http://tech.cnr.cn/digi/','http://tech.cnr.cn/techtx/','http://ent.cnr.cn/yaowen/','http://sports.cnr.cn/internal/China/','http://sports.cnr.cn/internal/csl/','http://sports.cnr.cn/internal/afc/','http://sports.cnr.cn/basket_ball/CBA/','http://sports.cnr.cn/basket_ball/NBA/','http://sports.cnr.cn/international/uefa/','http://sports.cnr.cn/international/England/','http://sports.cnr.cn/international/italy/','http://sports.cnr.cn/international/spanish/','http://sports.cnr.cn/tennis/news/','http://auto.cnr.cn/dbdg/','http://auto.cnr.cn/gcxc/','http://auto.cnr.cn/qczcjj/','http://travel.cnr.cn/2011lvpd/gny/','http://travel.cnr.cn/2011lvpd/cjy/','http://travel.cnr.cn/2011lvpd/zt/st/','http://travel.cnr.cn/2011lvpd/hangye/news/','http://edu.cnr.cn/ch/tj/','http://edu.cnr.cn/open/','http://edu.cnr.cn/lxcg/','http://edu.cnr.cn/lxcg/cg/','http://edu.cnr.cn/kaos/','http://edu.cnr.cn/wy/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="wh690 left"]//ul//li//a//@href').extract()
        for url in url:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//p[@class="f22 lh30 yahei"]/text()'))
        if not title:
            title = textify(hdoc.select('//div[@class="left yahei f22  lh24 fb"]//text()'))
        text = textify(hdoc.select('//div[@class="TRS_Editor"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="sanji_left"]//p/text()'))
        dt_added = textify(hdoc.select('//p[@class="lh30 left f14 yahei"]/text()')).split(' ')[0]
        if not dt_added:
            dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]/text()'))
        author = textify(hdoc.select('//span[@id="editor_baidu"]/text()'))
        if not author:
            author = textify(hdoc.select('//p[@class="right f16 lh32 yahei"]//text()'))
        if author:
            author = author.split(u'\uff1a')[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        if dt_added < get_current_timestamp()-86400*7:
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()

