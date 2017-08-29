from juicer.utils import *
from dateutil import parser

class AndhraPrabha(JuicerSpider):
    name ='andhra_prabha'
    start_urls=['http://www.prabhanews.com/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//li[contains(@class,"menu-")]/a/@href').extract()
        for link in links[:2]:
            yield Request(link,self.parse_articles,response)

    def parse_articles(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="view-content"]//div[contains(@class,"views-row")]//div[@class="cat-content"]')
        for node in nodes[:2]:
            date = textify(node.select('.//span[@class="date"]/text()'))
            date_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
            if date_added < get_current_timestamp()-86400*2:
                is_next = False
                continue
            news_link = textify(node.select('./h5/a/@href'))
            if 'http' not in news_link:news_link = 'http://www.prabhanews.com' + news_link
            yield Request(news_link,self.details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next last"]/a/@href'))
        if nxt_pg and is_next:
            nxt_pg = 'http://www.prabhanews.com' + nxt_pg
            yield Request(nxt_pg,self.parse_articles,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="heading"]/text()'))
        dt = textify(hdoc.select('//span[@class="posted"]/text()'))
        dt_added = get_timestamp(parse_date(dt) - datetime.timedelta(hours=5, minutes=30))
        text = textify(hdoc.select('//div[@class="view-content"]/div[contains(@class,"views-row")]/p//text()'))
        if title == '':import pdb;pdb.set_trace()
        if text == '':import pdb;pdb.set_trace()

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt',dt_added)
        item.set('text',xcode(text))
        #yield items.process()
