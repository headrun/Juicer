from juicer.utils import *
from dateutil import parser

class Szonline(JuicerSpider):
    name = "szonline_china"
    start_urls = ['http://focus.szonline.net/channel/3290.shtm','http://focus.szonline.net/channel/3235.shtm','http://focus.szonline.net/channel/3236.shtm','http://focus.szonline.net/channel/3237.shtm','http://focus.szonline.net/channel/3241.shtm','http://focus.szonline.net/channel/3243.shtm','http://focus.szonline.net/channel/1939.shtm','http://focus.szonline.net/channel/3238.shtm','http://focus.szonline.net/channel/3240.shtm','http://focus.szonline.net/channel/1938.shtm','http://focus.szonline.net/channel/2525.shtm','http://focus.szonline.net/channel/2528.shtm','http://focus.szonline.net/channel/2526.shtm','http://focus.szonline.net/channel/2527.shtm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="left"]//ul//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="acontent"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@class="btn_invite"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])
        yield item.process()

