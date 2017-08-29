from juicer.utils import*
from dateutil import parser

class JakartaPost_ID(JuicerSpider):
    name = 'jakarta_post'
    start_urls = ['http://www.thejakartapost.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[not(contains(@class, "tjp-li-7"))]/a[@class="tjp-has-submenu "]/@href').extract()
        for cat in categories:
            if 'http://www.jakartapostjobs.com' in cat or 'http://www.thejakartapost.com/most-viewed' in cat or '/most-shared' in cat:
                continue
            yield Request(cat,self.parse_mainlink,response)

    def parse_mainlink(self,response):
        hdoc = HTML(response)
        index_link = hdoc.select('//div[@class="top-latest-entry"]/h3/following-sibling::a[@class="seeall"]/@href').extract()
        if not index_link:
            is_nxt = True
            nodes = hdoc.select('//div[@class="col-xs-12 detail-latest"]')
            for node in nodes:
                date = textify(node.select('.//span[@class="date"]/span/text()'))
                if 'month ago' not in date:
                    date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
                    if date_added <  get_current_timestamp()-86400*30:
                        is_nxt = False
                        continue
                    link = textify(node.select('.//a[h5]/@href'))
                    yield Request(link,self.parse_details,response)

            nxt_pg = textify(hdoc.select('//div[@class="navigation-page"]/a[@class="jp-last"]/@href'))
            if 'http' not in nxt_pg: nxt_pg = 'http://www.thejakartapost.com' + nxt_pg
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_mainlink,response)
        yield Request(index_link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="detail-latest"]')
        for node in nodes:
            date = textify(node.select('.//span[contains(@class, "date today")]/span/text()'))
            if 'month ago' not in date:
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
                if date_added <  get_current_timestamp()-86400*30:
                    is_nxt =  False
                    continue

                link = textify(node.select('.//a[h5]/@href'))
                yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="navigation-page"]/a[@class="jp-last"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.thejakartapost.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)
        
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title-large"]//text()')) or textify(hdoc.select('//h3[@class="title-large"]//text()'))
        date = textify(hdoc.select('//span[@class="posting"]//span[@class="day"]/text() | //span[@class="posting"]//span[@class="time"]/text()')) or textify(hdoc.select('//span[@class="posted"]//span[@class="day"]/text() | //span[@class="posted"]//span[@class="time"]/text()'))
        if not date:
            date = textify(hdoc.select('//span[@class="posted clear"]/text()')) or textify(hdoc.select('//span[@class="day"]/text() | //span[@class="time"]/text()'))
            date = date.replace('Posted:','')
        text= textify(hdoc.select('//div[@id="show-bubb-text"]//p//text()')) or textify(hdoc.select('//div[@class="col-xs-12 list-multiple-page"]//p[not(a)]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//span[@class="name-post"]//text()'))
        if author:
            author_link = textify(hdoc.select('//span[@class="name-post"]/a/@href'))
            if 'http' not in author_link: author_link = 'http://www.thejakartapost.com' + author_link
        if author:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('author', {'name':xcode(author)})
            item.set('author_url',xcode(author_link))
            item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
            yield item.process()

        else:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
            yield item.process()

