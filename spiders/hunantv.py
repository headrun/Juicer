from juicer.utils import *
from dateutil import parser

class Hunantv(JuicerSpider):
    name = 'hunantv'
    start_urls = ['http://list.hunantv.com/10/-------------.html']

    def parse (self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//ul[@class="clearfix ullist-ele"]//li')

        for node in nodes[:3]:
           date = textify(node.select('.//p[@class="a-pic-t2"]/text()')).split(u'\u65f6\u95f4\uff1a')
           date = textify(date)
           date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
           if date_added <  get_current_timestamp()-86400*1:
               is_next = False
               continue
           news_links = textify(node.select('.//p[@class="a-pic-t1"]/a/@href'))
           yield Request(news_links,self.details,response,meta={'date_added':date_added})

        nxt_pg = textify(hdoc.select('//div[@class="mgtv-page clearfix"]/a[@class="btnr"]/@href'))
        if nxt_pg and is_next:
            nxt_pg_url = 'http://list.hunantv.com/10/' + nxt_pg
            yield Request(nxt_pg_url,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="play-index-til"]/text()'))
        dt_added = response.meta['date_added']
        tv_name = textify(hdoc.select('//div[@class="play-index-tiltag"]/a/text()')[0])
        tv_name_url = textify(hdoc.select('//div[@class="play-index-tiltag"]/a/@href')[0])
        if 'http' not in tv_name_url:
            tv_name_link = 'http://www.hunantv.com' + tv_name_url
        category = textify(hdoc.select('//div[@class="play-index-tiltag"]/a/text()')[-1])
        category_url = textify(hdoc.select('//div[@class="play-index-tiltag"]/a/@href')[-1])
        posted_by = textify(hdoc.select('//div[@class="play-index-tiltag"]/text()')[-1]).split('>')[-1]
        tv_info = {'name':tv_name,'url':tv_name_link}

        print '\n'
        print 'url:',response.url
        print 'title:',xcode(title)
        print 'dt_added',dt_added
        print 'tv_name:',xcode(tv_name)
        print 'tv_name_link:',tv_name_link
        print 'category:',xcode(category)
        print 'category_url:',category_url
        print 'posted_by:',xcode(posted_by)
        item = Item(response)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('posted',xcode(posted))
        item.set('url',response.url)
        item.set('tv_info',tv_info)
        item.set('xtags',['china_country_manual','news_sourcetype_manual'])
        #yield item.process()
