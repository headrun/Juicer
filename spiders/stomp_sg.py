from juicer.utils import*
from dateutil import parser
import time
import datetime


class Stomp_sg(JuicerSpider):
    name = 'stomp_sg'
    start_urls = ['http://www.stomp.com.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="menu nav navbar-nav"]//li[not(contains(@id, "mm-singapore-seen"))]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.stomp.com.sg' + cat
            if 'http://www.lollipop.sg/' in cat or 'http://www.stomp.com.sg/contribution/' in cat:
                continue
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="row category-top-story"] | //div[@class="category-listing-content"]')
        for node in nodes:
            is_nxt = True
            date = textify(node.select('.//div[@class="wsy-category"]//text()'))
            if date:
                date_dict = {'JANUARY':'1', 'FEBRUARY':'2','MARCH':'3','APRIL':'4','MAY':'5','JUNE':'6','JULY':'7','AUGUST':'8','SEPTEMBER':'9','OCTOBER':'10','NOVEMBER':'11','DECEMBER':'12'}
                month = date.split(' ')[0].strip()
                year = date.split(' ')[-1].strip()
                for key, value in date_dict.iteritems():
                    if key.lower() in month.lower():
                        month =month.lower().replace(key.lower(),value)
                        date = year + '-' + month
                date = datetime.datetime.strptime(date,'%Y-%m')
                date_added = int(time.mktime(date.timetuple()))
                if date_added < get_current_timestamp()-86400*30:
                    add_link = textify(node.select('.//h3/a[@target="_self"]/@href'))
                    if 'http' not in add_link: add_link = 'http://www.stomp.com.sg' + add_link
                    yield Request(add_link,self.parse_links,response)
                    is_nxt =  False
                    continue
        links = hdoc.select('//div[contains(@class, "category-")]//h3/a[@target="_self"]/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.stomp.com.sg' + link
            yield Request(link,self.parse_details,response)



        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.stomp.com.sg' + nxt_pg
        yield Request(nxt_pg,self.parse_links,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="field-item even"]/h1/text()'))
        text = textify(hdoc.select('//div[@class="field-item even"]//p[not(em)]//text()')) or textify(hdoc.select('//div[@class="ob-readmore-collapse field field-name-body field-type-text-with-summary field-label-hidden"]/p//text()')) or textify(hdoc.select('//div[@class="field-item even"]/p/span/text()'))
        date = textify(hdoc.select('//div[@class="submitted"]//text()'))
        date=date.split('|')[0].replace('Posted on ','')
        dt_added= get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags', ['news_sourcetype_manual', 'singapore_country_manual'])
#        yield item.process()
