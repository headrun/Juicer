from juicer.utils import *
from dateutil import parser

class CjnNews(JuicerSpider):
    name = "cjn_news"
    start_urls = ['http://news.cjn.cn/gnxw/','http://news.cjn.cn/jczt/index.htm','http://news.cjn.cn/gjxw/','http://news.cjn.cn/shxw/','http://entertainment.cjn.cn/yg/','http://entertainment.cjn.cn/musics/','http://entertainment.cjn.cn/ylyw2/','http://sport.cjn.cn/ttrd/','http://sport.cjn.cn/jcpl/','http://sport.cjn.cn/tysp/','http://sport.cjn.cn/ch/','http://finance.cjn.cn/gydky/','http://finance.cjn.cn/ph/','http://finance.cjn.cn/cfgs/','http://finance.cjn.cn/lctz/','http://finance.cjn.cn/msjj/','http://wenhua.cjn.cn/wtch/','http://wenhua.cjn.cn/wyyc/','http://wenhua.cjn.cn/mwrw/','http://wenhua.cjn.cn/cysl/','http://zx.cjn.cn/cj315/','http://www.cjdcw.com/zbxw/','http://www.cjdcw.com/csgh/','http://www.cjdcw.com/zcdx/','http://www.cjdcw.com/yjgd/','http://www.cjdcw.com/jjfs/','http://www.cjdcw.com/zxbd/','http://www.cjdcw.com/lslt/','http://news.cjn.cn/mtzq/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//section[@id="main-content"]//h2//a//@href')
        for url in urls:
            print url
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="TRS_Editor"]/p/text()')[:-1])
        if not text:
            text = textify(hdoc.select('//dic[@class="art-main"]/p/text()'))
        dt_added = textify(hdoc.select('//span[@class="pub-time"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//span[@class="hui1 lh29"]//text()'))
        #if date format is "05-05-2014" and day is the first then we have to
        #pass dayfirst=True to parse_date function
        # parse_date('05-07-2014') - Wrong
        #datetime.datetime(2014, 5, 7, 0, 0)
        #parse_date('05-07-2014', dayfirst=True) - Correct
        #datetime.datetime(2014, 7, 5, 0, 0)
        print "TITLE::::::::::::::::",xcode(title)
        print "TEXT:::::::::::::::::",xcode(text)
        print "DATE::::::::",xcode(dt_added)
        print "url:::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
       # item.set('author.name',xcode( author))
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])
        #yield item.process()

