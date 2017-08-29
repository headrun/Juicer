from juicer.utils import *

class NewsVn(JuicerSpider):
    name = 'news_vn'
    start_urls = 'http://news.go.vn/'

    def get_date(self,dt):
        if u'ph\xfat tr\u01b0\u1edbc' in dt:
            dt = dt.replace(u'ph\xfat tr\u01b0\u1edbc','minutes ago')
        elif u'gi\u1edd tr\u01b0\u1edbc' in dt:
            dt = dt.replace(u'gi\u1edd tr\u01b0\u1edbc','hours ago')
        elif u'h\xf4m qua' in dt:
            dt = dt.replace(u'h\xf4m qua','yesterday')
        return dt

    def parse(self,response):
        hdoc = HTML(response)
        cat_links = hdoc.select('//a[contains(@id,"menuid")]/@href | //div[@class="submenu"]/a/@href').extract()
        for cat_link in cat_links[:3]:
            yield Request(cat_link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        news_links = hdoc.select('//ul[@class="listnews_i"]/li[contains(@class,"cat_news")]')
        for news_link in news_links:
            dt = textify(news_link.select('./p[@class="time"]/text()'))
            dt = self.get_date(dt)
            date_added = get_timestamp(parse_date(dt))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue

            newslink = textify(news_link.select('./h2/a/@href'))
            yield Request(newslink,self.details,response)

        nxt_pg = textify(hdoc.select('//a[contains(text(),"Trang sau")]/@href'))
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse_links,response)

        next_pg = textify(hdoc.select('//li[@class="title"]/h3/a/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse_links,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="titleNews"]/text()'))
        date = textify(hdoc.select('//span[@class="date"]/text()'))
        if  u'ph\xfat tr\u01b0\u1edbc' in date or u'gi\u1edd tr\u01b0\u1edbc' in date:
            date = self.get_date(date)
            dt_added = get_timestamp(parse_date(date))
        elif u'h\xf4m qua' in date:
            date = textify(hdoc.select('//time[@itemprop="datePublished"]/@datetime')).split('T')[0]
            dt_added = get_timestamp(parse_date(date,dayfirst=True)-datetime.timedelta(hours=7))
        else:
            dt_added = get_timestamp(parse_date(date,dayfirst=True)-datetime.timedelta(hours=7))
        text = textify(hdoc.select('//div[@itemprop="articleBody"]//text()')) #or textify(hdoc.select('//div[@id="main-detail"]//text()'))
        if title =='' or text =='':import pdb;pdb.set_trace()
        
        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'date',xcode(date)
        print 'text',xcode(text)
