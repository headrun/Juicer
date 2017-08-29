from juicer.utils import *
from dateutil import parser
#from scrapy.item import Item, Field

class Beritaharian(JuicerSpider):
    name = 'beritaharian'
    start_urls = ['http://www.beritaharian.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "leaf")]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.beritaharian.sg' + cat
            if '/sph.com.sg/' in cat or 'specials.beritaharian.sg' in cat:
                continue
            yield Request(cat,self.parse_links,response)
 
    def parse_links(self,response):
        hdoc = HTML(response)
        news_lnk = textify(hdoc.select('//a[@class="btn"]/@href')) or textify(hdoc.select('//li[@class="leaf active"]/a/@href')) or textify(hdoc.select('//li[@class="last leaf"]/a/@href'))
        if 'http' not in news_lnk: news_lnk = 'http://www.beritaharian.sg' + news_lnk
        yield Request(news_lnk,self.parse_main_links,response)


    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="group-media-body media-body"]')
        for node in nodes:
            date = textify(node.select('./text()'))
            date_added= get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h3/a/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.beritaharian.sg' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="headline node-title"]/text()'))
        date = textify(hdoc.select('//div[@class="field field-name-post-date field-type-ds field-label-hidden"]//div[@class="field-item even"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text =textify(hdoc.select('//div[@class="odd field-item"]//p//text()'))
        text = text.replace('Langgani BeritaHarian.sg untuk menikmati laporan ini. Sila DAFTAR untuk teruskan.','')
        text1 = textify(hdoc.select('//h2[@class="node-subheadline"]/text()'))
        text_final = text1 + text
        author = textify(hdoc.select('//div[@class="author-field author-name"]//text()')) or  textify(hdoc.select('//h2[@class="node-subheadline"]//text()'))
        author_url = textify(hdoc.select('//div[@class="author-field author-name"]/a/@href'))
        if 'http' not in author_url: author_url = 'http://www.beritaharian.sg' + author_url
    
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text_final))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','singapore_country_manual'])
        yield item.process()
