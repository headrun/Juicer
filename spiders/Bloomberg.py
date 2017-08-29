from juicer.utils import*
from dateutil import parser

class Bloomberg(JuicerSpider):
    name = 'bloomberg'
    start_urls = ['http://www.bloomberg.com/asia']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="bb-nav-categories__category-container"]/a/@href').extract() + hdoc.select('//li[@class="bb-nav-submenu__category"]/a/@href').extract()
        for category in categories:
            yield Request(category,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//a[@data-resource-type="article"]/@href').extract() + hdoc.select('//div[@class="news__story__headline"]/a/@href').extract()
        for link in links:
            if 'http:' not in link:
                link = 'http://www.bloomberg.com/'+link
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="lede-headline"]/span//text()'))
        text = textify(hdoc.select('//span[@class="lede-dek__text"]/text()')) +  textify(hdoc.select('//div[@class="article-abstract__item-text"]/text()'))+textify(hdoc.select('//div[@class="article-body__content"]/p//text()'))  or textify(hdoc.select('//span[@class="lede-dek__text"]/text()'))+ textify(hdoc.select('//div[@class="article-abstract__item-text"]/text()')) + textify(hdoc.select('//div[@class="article-body__content"]/p//text()'))
        author = textify(hdoc.select('//a[@class="author-link"]/text()'))
        author_link = textify(hdoc.select('//div[@class="author-byline"]/a[contains(@href,"authors")]/@href').extract())
        date = textify(hdoc.select('//div[@class="published-info"]/time/@datetime'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'author_link',xcode(author_link)
        print 'dt_added',xcode(dt_added)

