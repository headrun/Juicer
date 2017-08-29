from juicer.utils import*
from dateutil import parser

class AbsNews(JuicerSpider):
    name = "abs_news"
    start_urls = ['http://news.abs-cbn.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="header-nav"]//li[not(contains(@class,"active"))]/a/@href').extract()
        for category in categories:
            if 'http' not in category: category = 'http://news.abs-cbn.com' + category
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[contains(@class,"col-9 content")]')
        for node in nodes:
            date = node.select('.//span[@class="datetime"]/text()').extract()[0]
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('.//p[@class="title"]/a/@href'))
            if 'http' not in link: link = 'http://news.abs-cbn.com' + link
            yield Request(link,self.parse_details,response)

        next_page = textify(hdoc.select('//a[contains(@title,"Next")]/@href'))
        if next_page and is_next:
            next_page = 'http://news.abs-cbn.com' + next_page
            yield Request(next_page,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="news-title"]/text()'))
        text = textify(hdoc.select('//div[@itemprop="articleBody"]/p//text()'))
        author = textify(hdoc.select('//span[@class="editor"]/text()'))
        if ',' in author:
            author = author.split(',')[0].strip()
        date = hdoc.select('//span[@class="date-posted"]/text()').extract()[0]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set(url, response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('author.name',xcode(author)
        item.set('dt_added',xcode(dt_added))
