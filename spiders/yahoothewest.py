from juicer.utils import *
from dateutil import parser

class AuYahoowest(JuicerSpider):
    name = 'yahoothewest'
    start_urls = ['https://au.news.yahoo.com/thewest/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[contains(@class, "dnav-tier dnav-tier-")]//li/a/@href')
        for category in categories[:3]:
            yield Request(category, self.parse_details,response)
            import pdb;pdb.set_trace()
    def parse_details(self,response):        
        hdoc = HTML(response)
        links = hdoc.select('//h3[@class="collection-title"]/a/@href')
        for link in links:
            yield Request(link, self.parse_news_information, response)

    def parse_news_information(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="page-header-content"]/h1/text()')) or textify(hdoc.select('//header[@class="module-header"]/h2/text()'))
        text = textify(hdoc.select('//div[@class="article-container"]//p/text()'))
        author = textify(hdoc.select('//span[contains(@class, "article-byline-")]/text()'))
        date = textify(hdoc.select('//time[@class="article-byline-time"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'author', xcode(author)
        print 'dt_added', xcode(dt_added)





