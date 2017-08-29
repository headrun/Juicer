from juicer.utils import *
from dateutil import parser

class Independent_sg(JuicerSpider):
    name = 'independent'
    start_urls = ['http://theindependent.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@id="td-header-menu"]//li[contains(@class, "menu-item menu-item")]/a/@href').extract()
        for cat in categories[:2]:
            if 'http://theindependent.sg/my/' in cat:
                continue
            yield Request(cat,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[contains(@class, "td_module")]')
        for node in nodes:
            date = textify(node.select('.//div[@class="td-post-date"]/time[@itemprop="dateCreated"]/text()'))
            if date:
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt =  False
                    continue
            link =  list(set(node.select('.//a[@rel="bookmark"]/@href').extract()))
            link = 'http://www.theindependent.sg/raspreet-is-an-america-first-in-singapore-football/'
            if 'http://theindependent.sg/my/' in link:
                continue
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[i[@class="td-icon-menu-right"]]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
       hdoc = HTML(response)
       title = textify(hdoc.select('//h1[@class="entry-title"]/text()')) or textify(hdoc.select('//h1[@class="entry-title"]//text()'))
       text = textify(hdoc.select('//div[@class="td-post-content"]//p//text() | //div[@class="td-post-content"]//blockquote//text()'))
       if 'Read also:' in text:
           text = text.encode('utf-8').split('Read also:')[0]
       author = textify(hdoc.select('//div[@class="td-g-rec td-g-rec-id-content_top "]/following-sibling::p[1]/span/text()'))
       date  = textify(hdoc.select('//span[@class="td-post-date"]//text()'))
       dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
       import pdb;pdb.set_trace()      
       item = Item(response)
       item.set('url',response.url)
       item.set('title',xcode(title))
       item.set('text',xcode(text))
       item.set('dt_added',xcode(dt_added))
       item.set('author',{'name':xcode(author)})
       item.set('author_url',xcode(auth_url))
       item.set('xtags', ['news_sourcetype_manual', 'singapore_country_manual'])
       yield item.process()
