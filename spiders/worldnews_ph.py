from juicer.utils import *
from dateutil import parser

class WorldNewsPH(JuicerSpider):
    name = 'worldnews_ph'
    start_urls = ['http://www.worldnews.net.ph/category/she-lun','http://www.worldnews.net.ph/category/ben-dao','http://www.worldnews.net.ph/category/hua-she','http://www.worldnews.net.ph/category/guo-ji','http://www.worldnews.net.ph/category/jing-ji','http://www.worldnews.net.ph/category/bao-dao','http://www.worldnews.net.ph/category/yu-le','http://www.worldnews.net.ph/category/ti-yu','http://www.worldnews.net.ph/category/wen-yi','http://www.worldnews.net.ph/category/guang-chang','http://www.worldnews.net.ph/category/qi-ta']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//div[@class="posts-list listing-alt"]//div[@class="content"]')

        for link in links:
            import pdb;pdb.set_trace()
            dt = textify(link.select('./time/text()'))
            date_added = get_timestamp(parse_date(xcode(dt))-datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            newslink = textify(link.select('./a/@href'))
            yield Request(newslink,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]/li/a[@rel="next"]/@href'))
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name headline"]/text()'))
        text = textify(hdoc.select(' //h4/text() | //div[@itemprop="articleBody"]//text()'))
        dt_added = textify(hdoc.select('//time[@itemprop="datePublished"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added))-datetime.timedelta(hours=8))
"""
        item = Item()response
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
"""
