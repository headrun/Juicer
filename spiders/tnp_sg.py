from juicer.utils import *
from dateutil import parser

class TnpSg(JuicerSpider):
    name = "tnp_sg"
    start_urls = ['http://www.tnp.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = set(hdoc.select('//ul//li[contains(@class, "leaf menu-nav--")]/a/@href').extract())
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.tnp.sg' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="card clearfix"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="card-footer"]/time//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h2[@class="card-title"]/a/@href'))
            if 'http' not in link: link = 'http://www.tnp.sg' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next"]//a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.tnp.sg' + nxt_pg
        if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[contains(@class,"headline")]/text()'))
        text = textify(hdoc.select('//div[@class="body-copy"]//p//text()'))
        date = textify(hdoc.select('//div[contains(@class, "field-name-post-date")]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="byline-name"]//text()'))     
        auth_url = textify(hdoc.select('//div[@class="byline-name"]//a/@href'))
        if 'http' not in auth_url: auth_url = 'http://www.tnp.sg' + auth_url

"""
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author'{'name':xcode(author)})
        item.set('author_url',xcode(auth_url))
        item.set('xtags',['news_sourcetype_manual','singapore_country_manual'])
        yield item.process()


"""
