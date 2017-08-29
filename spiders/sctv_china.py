from juicer.utils import *
from dateutil import parser

class Sctv(JuicerSpider):
    name = "sctv_china"
    start_urls = ['http://tf.sctv.com/scszyw/index.shtml','http://tf.sctv.com/shxw/index.shtml','http://tf.sctv.com/szxw/index.shtml','http://tf.sctv.com/jjxw/index.shtml','http://tf.sctv.com/zwxx/index.shtml','http://tf.sctv.com/scpdpl/index.shtml','http://ent.sctv.com/ylsy/xyxy/','http://ent.sctv.com/DY/','http://ent.sctv.com/ds/','http://ent.sctv.com/YY/','http://ent.sctv.com/ylpdpl/','http://ent.sctv.com/MXBG/','http://news.sctv.com/plpd/gnxwpl/','http://news.sctv.com/plpd/gjzsfx/','http://news.sctv.com/plpd/sh/','http://news.sctv.com/plpd/RW/','http://news.sctv.com/plpd/ty/','http://news.sctv.com/plpd/cj/','http://news.sctv.com/plpd/jy/','http://news.sctv.com/plpd/kjpl/','http://news.sctv.com/plpd/jspl/','http://news.sctv.com/plpd/ylpl/','http://news.sctv.com/plpd/scpl/','http://news.sctv.com/gnxw/szyw/index.shtml','http://news.sctv.com/gnxw/rdxw/index.shtml','http://news.sctv.com/gnxw/gat/index.shtml','http://news.sctv.com/gnxw/sdbd/index.shtml','http://news.sctv.com/plpd/gnxwpl/index.shtml','http://news.sctv.com/shxw/msmy/index.shtml','http://news.sctv.com/shxw/shfz/index.shtml','http://news.sctv.com/plpd/sh/index.shtml','http://news.sctv.com/shxw/zqrs/index.shtml','http://news.sctv.com/shxw/sjwx/index.shtml','http://news.sctv.com/kjxw/qy/index.shtml','http://news.sctv.com/kjxw/cy/index.shtml','http://news.sctv.com/kjxw/kp/index.shtml','http://news.sctv.com/kjxw/tm/index.shtml']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list2"]//ul//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="texttitle"]//text()'))
        text = textify(hdoc.select('//div[@class="TRS_Editor"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="textproperty"]//text()')[2])
        dt_added = dt_added.split(u'\uff1a')
        dt_added = dt_added[1]
        author = textify(hdoc.select('//div[@class="ep-editor-layout"]//text()'))
        author = author.split("document.write(")[1].split(")")[0]
        author = author.replace("<br/>'", " ").split(u'\uff1a')[1].strip()
        if not author:
            author = textify(hdoc.select('//div[@class="ep-editor-layout"]//text()'))
            author = author.split("document.write(")[2]
            author = author.replace("');", " ").split(u'\uff1a')[1].strip()
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()
