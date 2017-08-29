from juicer.utils import *
from dateutil import parser

class Ofweek(JuicerSpider):
    name = "ofweek_china"
    start_urls = ['http://www.ofweek.com/CATListNew-41000-74002.html','http://www.ofweek.com/CATListNew-41000-74003.html','http://www.ofweek.com/CATListNew-25000-74004.html','http://www.ofweek.com/CATList-8300-JISHUYINYONG.html','http://www.ofweek.com/CATListNew-74000-0.html','http://www.ofweek.com/CATListNew-41000-75008.html','http://www.ofweek.com/CATListNew-25000-8000.html','http://www.ofweek.com/CATListNew-25000-10000.html','http://www.ofweek.com/CATListNew-29000-19000.html','http://finance.ofweek.com/finance/75011/100/100.html','http://www.ofweek.com/CATListNew-73000-0.html','http://www.ofweek.com/CATList-8400-SHICHANGYUANJIU.html','http://www.ofweek.com/CATList-8200-CHANGPINGXINXIT.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list-left"]//h3//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@id="articleC"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@class="sdate"]//text()'))
        author = textify(hdoc.select('//div[@class="bianji"]//span//text()'))
        author = author.split(u'\uff1a')[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

