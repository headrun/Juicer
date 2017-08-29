from juicer.utils import *
from dateutil import parser

class BorderwatchAu(JuicerSpider):
    name = 'borderwatch'
    start_urls = ['http://www.borderwatch.com.au/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [500]

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "cat-item cat-item-")]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

    """
    start_urls = ['http://www.borderwatch.com.au/news/','http://www.borderwatch.com.au/sport/','http://www.borderwatch.com.au/community/','http://www.borderwatch.com.au/life-style/','http://www.borderwatch.com.au/entertainment/','http://www.borderwatch.com.au/multimedia/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//article[@class="wrapper left"]')

        for node in nodes:
            dt = textify(node.select('.//time[@datetime]/text()'))
            date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue

            link = textify(node.select('.//h3/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@rel="next"]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://www.borderwatch.com.au' + nxt_pg
            yield Request(nxt_pg,self.parse,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name"]/text()'))
        text = textify(hdoc.select('//div[@id="mrec-story-bottom"]/following-sibling::p[not(contains(text(), "The story "))]/text()'))
        date = textify(hdoc.select('//time[@itemprop="datePublished"]/text()'))
        author = textify(hdoc.select('//span[@class="story-header__author-name story-header__author-byline"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))
        item = Item(response)
        item.set('url',response.url)
        item.set('title' ,xcode(title))
        item.set('text' ,xcode(text))
        item.set('author', xcode(author))
        item.set('dt_added' ,xcode(dt_added))
        yield item.process()
        """
