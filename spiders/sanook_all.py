from juicer.utils import *
from dateutil import parser

class  SanookAll(JuicerSpider):
    name = "sanook_all"
    start_urls = ['http://auto.sanook.com/archive/','http://news.sanook.com/archive/','http://news.sanook.com/archive/world/','http://news.sanook.com/archive/region/','http://sport.sanook.com/archive/','http://news.sanook.com/archive/social/','http://news.sanook.com/archive/crime/','http://news.sanook.com/archive/entertain/','http://news.sanook.com/tag/%E0%B8%9A%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%97%E0%B8%B4%E0%B8%87%E0%B8%AE%E0%B8%AD%E0%B8%95%E0%B8%9B%E0%B8%B1%E0%B8%81%E0%B8%AB%E0%B8%A1%E0%B8%B8%E0%B8%94/','http://news.sanook.com/archive/talkofthetown/','http://news.sanook.com/archive/politic/','http://campus.sanook.com/archive/teenzone/intrend/latest/all/','http://campus.sanook.com/archive/teenzone/star/latest/all/','http://campus.sanook.com/archive/teenzone/globalwarming/latest/all/','http://campus.sanook.com/archive/education/scholarship/','http://campus.sanook.com/archive/education/specialcourse/latest/all/','http://campus.sanook.com/archive/education/abroad/latest/all/']


    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//article[@class="post post--list post--archive"]') or hdoc.select('//div[@class="result-article"]')
        for node in nodes:
            date = textify(node.select('.//time[@class="post__meta"]/@datetime'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a[@title]/@href'))
            yield Request(link,self.parse_details,response)
            if not date:
                date = textify(node.select('.//span[@class="date-time"]//text()')) 
                if u'\u0e2a.\u0e04.' in date or u'\u0e19.' in date or u'\u0e01.\u0e04.' in date or u'\u0e40\u0e21.\u0e22.' in date:
                    dt1 = date.replace(u'\u0e2a.\u0e04.','aug').replace(u'\u0e19.','AM').replace(u'\u0e01.\u0e04.','july').replace(u'\u0e40\u0e21.\u0e22.','april')
                if 'aug 60' in dt1 or 'july 60' in dt1 or 'april 59' in dt1:
                    dt = dt1.replace('aug 60','aug 06').replace('july 60','july 06').replace('april 59','april 09')

                date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./h2/a[img]/@href'))
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//div[@class="ugc-paging"]//a[contains(.,">")]/@href'))
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse,response)

        if not nodes:
            links = hdoc.select('//div[@class="_fchild-fl-mg_r10x"]//h2/a/@href').extract()
            for lin in links:
                yield Request(lin,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//nav[@class="pagination alpha"]//a[@class="pagination__item pagination__item--next pagination__link"]/@href')) or textify(hdoc.select('//div[@class="_child-dp_inblock-pd_s5x"]//a[contains(.,"%s")]/@href'%u'\u0e16\u0e31\u0e14\u0e44\u0e1b'))
        if u'\u0e1a\u0e31\u0e19\u0e40\u0e17\u0e34\u0e07\u0e2e\u0e2d\u0e15\u0e1b\u0e31\u0e01\u0e2b\u0e21\u0e38\u0e14' in nxt_pg:
            nxt_pg = nxt_pg.replace(u'\u0e1a\u0e31\u0e19\u0e40\u0e17\u0e34\u0e07\u0e2e\u0e2d\u0e15\u0e1b\u0e31\u0e01\u0e2b\u0e21\u0e38\u0e14', '%E0%B8%9A%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%97%E0%B8%B4%E0%B8%87%E0%B8%AE%E0%B8%AD%E0%B8%95%E0%B8%9B%E0%B8%B1%E0%B8%81%E0%B8%AB%E0%B8%A1%E0%B8%B8%E0%B8%94')
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="content__title sukhumvitbold"]//text()'))
        date=textify(hdoc.select('//time[@itemprop="dateCreated"]/@datetime'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@id="content__page--1"]//p//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','thailand_country_manual'])
        yield item.process()


