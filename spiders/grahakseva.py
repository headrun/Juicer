import time
import re
from juicer.utils import *
from dateutil import parser

class Grahak_Seva(JuicerSpider):
    name="grahakseva"
    start_urls = ['http://www.grahakseva.com/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@style="margin-bottom:20px"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="user-meta user-default-icon"]//text()'))
            date=''.join(re.findall(' on (.*)', date))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h1/a/@href'))
            if 'http' not in link: link = 'http://www.grahakseva.com' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//span[@class="pg-cell"]/a[contains(text(),"Next")]/@href'))
        if 'http' not in  nxt_pg: nxt_pg = 'http://www.grahakseva.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select("//h1[@class='cpage-heading unsel']/text()"))
        text = textify(hdoc.select("//div[@class='complaints']/div[@class='desc']/p//text()"))
        author_name_and_posted_date = hdoc.select('//div[@class="user-meta user-default-icon"]/text()')
        if not author_name_and_posted_date:
            author_name_and_posted_date = hdoc.select('//div[contains(@class,"user-meta")][1]/text()')
        author_name = ''.join(re.findall('(.*) on ',textify(author_name_and_posted_date)))
        date = ''.join(re.findall(' on (.*)',textify(author_name_and_posted_date)))
        date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        


        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(date_added))
        item.set('author', {'name':xcode(author_name)})
        item.set('xtags',['forums_sourcetype_manual','india_country_manual'])
        yield  item.process()
