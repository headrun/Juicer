from juicer.utils import *
from dateutil import parser

class S1979(JuicerSpider):
    name = "s1979_china"
    start_urls = ['http://www.s1979.com/news/china/','http://www.s1979.com/news/world/','http://www.s1979.com/news/society/','http://www.s1979.com/caijing/','http://www.s1979.com/shenzhen/shehui/','http://www.s1979.com/shenzhen/shishi/','http://www.s1979.com/shenzhen/paihang/','http://www.s1979.com/shenzhen/yueyu/','http://www.s1979.com/shenzhen/living/','http://www.s1979.com/shenzhen/yule/','http://www.s1979.com/media/net/','http://www.s1979.com/media/it/','http://www.s1979.com/media/news/','http://www.s1979.com/media/renwu/','http://www.s1979.com/media/commerce/','http://www.s1979.com/media/wei/','http://www.s1979.com/media/guancha/','http://www.s1979.com/gangaotai/list_48_1.shtml']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list-column clearfix"]//ul//li//h1//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="article-text"]/p/text()'))
        if not text:
            text =textify(hdoc.select('//div[@class="image-text clearfix"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="article-published"]/span[@class="mlr10"]/text()')[0])
        dt_added = dt_added.split(u'\uff1a')
        if len(dt_added) is 2:
            dt_added.pop(0)
            dt_added = ''.join(dt_added)
        else:
            dt_added = ''.join(dt_added)
       #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        print "TITLE::::::::::::::::",xcode(title)
        print "TEXT:::::::::::::::::",xcode(text)
        print "DATE::::::::",xcode(dt_added)
        print "url:::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        #yield item.process()

