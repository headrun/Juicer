from juicer.utils import *
from dateutil import parser

class BangloreTimes(JuicerSpider):
    name = "banglore_times"
    start_urls = ['http://www.thebangaloretimes.com/bengaluru','http://www.thebangaloretimes.com/dakshina-kannada','http://www.thebangaloretimes.com/kerala','http://www.thebangaloretimes.com/karnataka','http://www.thebangaloretimes.com/goa','http://www.thebangaloretimes.com/middle-east','http://www.thebangaloretimes.com/world','http://www.thebangaloretimes.com/sports','http://www.thebangaloretimes.com/health']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="news_linsting_inner ovr"]//div[@class="single_news_display_section"]//h2//a//@href')
        for url in urls:
            yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="hedding-main-page ovr"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="description ovr"]//p//text()'))
        dt_added= textify(hdoc.select('//label[@class="date-news-page fr"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item =Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set("dt_added",dt_added)
        item.set('url', response.url)
        yield item.process()

