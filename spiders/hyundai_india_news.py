from juicer.utils import *
from dateutil import parser

class HyundaiIndiaNews(JuicerSpider):
    name = 'hyundai_india_news'
    start_urls = ['http://www.hyundai.com/in/en/MediaCenter/GlobalNews/index.html','http://www.hyundai.com/in/en/MediaCenter/PressReleases/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="global_news"]//div[@class="news_list"]//h2//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2//text()'))
        text1 = textify(hdoc.select('//ul[@class="em"]//li//text()'))
        text = textify(hdoc.select('//div[@class="text"]//p//text()'))
        text = text1 +  '\n' + text
        dt_added = textify(hdoc.select('//span[@class="date"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()


