from juicer.utils import *
from dateutil import parser

class StdHk(JuicerSpider):
    name = 'std_hk'
    start_urls = ['http://std.stheadline.com/instant/articles/listview/%E9%A6%99%E6%B8%AF/', 'http://std.stheadline.com/instant/articles/listview/%E5%9C%8B%E9%9A%9B/', 'http://std.stheadline.com/instant/articles/listview/%E4%B8%AD%E5%9C%8B/', 'http://std.stheadline.com/instant/articles/listview/%E7%B6%93%E6%BF%9F/', 'http://std.stheadline.com/instant/articles/listview/%E5%9C%B0%E7%94%A2/', 'http://std.stheadline.com/instant/articles/listview/%E9%AB%94%E8%82%B2/', 'http://std.stheadline.com/instant/articles/listview/%E5%A8%9B%E6%A8%82/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="news-wrap"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="time"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added< get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            newslink = textify(node.select('./a/@href'))
            newslink = 'http://std.stheadline.com/'+ newslink.split('/../')[-1]
            if 'http' not in newslink:newslink = 'http://std.stheadline.com' + newslink
            yield Request(newslink,self.details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination pagination-md"]//a[@rel="next"]/@href'))
        if u'\u9999\u6e2f' in nxt_pg or u'\u5730\u7522' in nxt_pg or u'\u570b\u969b'  in nxt_pg or u'\u4e2d\u570b' in nxt_pg or u'\u9ad4\u80b2' in nxt_pg or u'\u5a1b\u6a02' in nxt_pg:
            nxt_pg = nxt_pg.replace(u'\u9999\u6e2f','%E9%A6%99%E6%B8%AF').replace(u'\u5730\u7522','%E5%9C%B0%E7%94%A2').replace(u'\u570b\u969b','%E5%9C%8B%E9%9A%9B').replace(u'\u4e2d\u570b','%E4%B8%AD%E5%9C%8B').replace(u'\u9ad4\u80b2','%E9%AB%94%E8%82%B2').replace(u'\u5a1b\u6a02','%E5%A8%9B%E6%A8%82')
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)


    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="post-heading supplement-p-h"]/h1/text()'))
        dt = textify(hdoc.select('//div[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="paragraph"]/p/text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        item.set('xtags',['news_sourcetype_manual','hong_kong_country_manual'])
        yield item.process()
