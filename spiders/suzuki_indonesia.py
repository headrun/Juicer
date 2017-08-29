from juicer.utils import *
from dateutil import parser

class SuzukiIndonesia(JuicerSpider):
    name = 'suzuki_indonesia'
    start_urls = ['http://www.suzuki.co.id/suzuki_news_list.php?yearz=2014']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//a[@class="contentTextJustify01"]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td[@class="contentTextJustify01"]/b/text()'))
        text = textify(hdoc.select('//td[@class="contentTextJustify01"]/p/text()'))
        if not text:
            text = textify(hdoc.select('//td[@class="contentTextJustify01"]/text()')[1:])
        dt_added = textify(hdoc.select('//td[@class="contentTextJustify01"]/text()')[0])
        dt_added = get_timestamp(parse_date(dt_added, dayfirst=True) - datetime.timedelta(hours=8))
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()


