from juicer.utils import *
from dateutil import parser

class NOVnews(JuicerSpider):
    name = "nov_news"
    start_urls = ['http://nvonews.com/category/business/','http://nvonews.com/category/health/','http://nvonews.com/category/life-style/','http://nvonews.com/category/daily-news/','http://nvonews.com/category/national/','http://nvonews.com/category/sports/','http://nvonews.com/category/tourism/','http://nvonews.com/category/world-news/','http://nvonews.com/category/environment/']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[contains(@class, "widget-full-list-text")]/a/@href')
        for url in urls:
            yield Request(url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="story-title entry-title"]/text()'))
        extra_text = textify(hdoc.select('//div[@id="content-area"]//strong/text()'))
        text = textify(hdoc.select('//div[@id="content-area"]/p/text()'))
        final_txt = extra_text + ' ' + text
        dt_added1 = textify(hdoc.select('//span[@id="artdate"]//text()')) or hdoc.select('//span[@class="post-date"]//text()').extract()[0]
        dt_added = get_timestamp(parse_date(dt_added1) - datetime.timedelta(hours=5, minutes=30))

        if date_added > get_current_timestamp()-86400*30:
            item = Item(response)
            item.set('title', xcode(title))
            item.set('text', xcode(final_txt))
            item.set('dt_added', dt_added)
            item.set('url', response.url)
            yield item.process()
