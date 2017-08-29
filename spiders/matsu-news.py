from juicer.utils import *
from dateutil import parser
from scrapy.http import FormRequest

class MatsuNews(JuicerSpider):
    name = 'matsu_news'
    start_urls = 'http://www.matsu-news.gov.tw/2010web/news_101.php'

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//tr[@valign="middle"]')
        try:number=response.meta['number'] + 25
        except:number = 25
        for link in links:
            date = textify(link.select('./td/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*2:
                is_next = False
                continue
            news_link = textify(link.select('./td/a/@href'))
            yield Request(news_link,self.parse_details,response)
        url = response.url
        uniqvalue = u'\u4e0b\u4e00\u9801'
        nxt_pg = hdoc.select('//input[@type="button"][contains(@value,uniqvalue)]/@type')

        if nxt_pg and is_next:yield FormRequest(url,self.parse,formdata={'UID':'','CMD':'','from':str(number),'mode':'','type':'','year':'','month':'','day':'','keyword':''},meta={'number':number})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//font[@class="title7"]/text()'))
        dt = textify(hdoc.select('//font[@class="title7"]/parent::td/text()'))
        date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
        text= textify(hdoc.select('//div[@id="Zoom"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',date_added)
        item.set('text',xcode(text))
