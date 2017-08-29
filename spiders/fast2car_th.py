from juicer.utils import *
from dateutil import parser

class Fast2carThailand(JuicerSpider):
    name = 'fast2car_th'
    start_urls = ['http://www.fast2car.com/car.php?year=%3E2010']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="main"]/div[@class="body"]')

        for node in nodes:
            date = textify(node.select('.//div[@class="update2"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=7))
            if dt_added < get_current_timestamp()-86400*30:
                continue
            link = textify(node.select('.//div[contains(@class,"name")]/a[@title]/@href'))
            link = 'http://www.fast2car.com/%E0%B8%A3%E0%B8%96%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%AD%E0%B8%87,TOYOTA-ALTIS-1.8-[E]-%E0    %B8%9B%E0%B8%B5-2011,123421.html'
            yield Request(link,self.parse_details,response,meta={'dt_added':dt_added})

        nxt_pg = textify(hdoc.select('//div[@class="next_pagenum"]/a/@href').extract()[0])
        if 'http'not in nxt_pg:
            nxt_pg = 'http://www.fast2car.com/car.php' + nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="name"]/h1/text()').extract()[0])
        number = textify(hdoc.select('//div[@class="number"]/text()').extract()[0])
        price = textify(hdoc.select('//span[@class="price"]/text()')) or textify(hdoc.select('//div[@class="header"]/div[@class="number"]/span/text()'))
        specifications = textify(hdoc.select('//div[@class="header-bar car-detail"]/parent::div//div[@class="spec"]//text()'))
        options = textify(hdoc.select('//div[@class="header-bar car-detail"]/parent::div//div[@class="option"]//text()'))
        finance_details = textify(hdoc.select('//div[@class="header-bar finance"]/parent::div//div[@class="spec"]//text()'))
        seller_info = textify(hdoc.select('//div[@class="header-bar seller"]/parent::div//div[@class="spec"]//text() | //div[@class="header-bar seller"]/parent::div//div[@class="option"]//text()'))
        car_details = textify(hdoc.select('//div[@id="same-model"]//div[@class="body"]/text()'))

        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(specifications + ' '  + options + ' ' + finance_details + ' ' + seller_info + ' ' + car_details)
        print 'date',response.meta['date']
        print 'price',xcode(price)
        print 'number',xcode(number)
''' 

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',response.meta['dt_added'])
        item.set('price',xcode(price))
        item.set('number',xcode(number))
        item.set('text' , xcode(specifications + ' '  + options + ' ' + finance_details + ' ' + seller_info + ' ' + car_details))
        item.set('xtags',['blogs_sourcetype_manual','thailand_country_manual'])
        yield item.process()'''
