from juicer.utils import *
from dateutil import parser

class Malaya_ph(JuicerSpider):
    name = 'malaya'
    start_urls = ['http://www.malaya.com.ph/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@id="block-nice-menus-1"]//li[contains(@class, "menuparent")]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="latest-teaser"]')
        for node in nodes:
            date = textify(node.select('.//div[@id="author-info"]/text()'))
            date = ''.join(re.findall('(\w+ \d+, \d+)', date))
            if date:
                dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
                if dt_added < get_current_timestamp()-86400*30:
                    is_next = False
                    continue
            link = textify(node.select('./h3[@id="teaser-title"]/a/@href'))
            yield Request(link,self.parse_details,response)   
        nxt_pgs= textify(hdoc.select('//li[@class="pager-next"]/a/@href'))
        if 'http' not in nxt_pgs: nxt_pgs = 'http://www.malaya.com.ph' + nxt_pgs
        if nxt_pgs and is_next:
            yield Request(nxt_pgs,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title"]/text()'))
        text = textify(hdoc.select('//div[@property="content:encoded"]//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="field-item even"]/div/text()')) or textify(hdoc.select('//div[@class="field-item even"]/p//text()'))
        date = textify(hdoc.select('//span[@property="dc:date dc:created"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="name"]//text()'))
        author = author.replace('By','')
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace
        
        """item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','philippines_country_manual'])
        #yield item.process()
"""
