from juicer.utils import *
from dateutil import parser

class StvCn(JuicerSpider):
    name = 'sctv_china'
    start_urls = ['http://www.sctv.com/news/gn/']#,'http://www.sctv.com/news/world/','http://www.sctv.com/news/society/','http://www.sctv.com/news/ent/','http://www.sctv.com/news/mil/','http://www.sctv.com/news/sports/','http://www.sctv.com/news/finance/','http://www.sctv.com/news/comment/','http://www.sctv.com/news/funny/','http://www.sctv.com/news/law/','http://www.sctv.com/news/commonweal/','http://www.sctv.com/sc/my/','http://www.sctv.com/sc/dy/','http://www.sctv.com/sc/ga/','http://www.sctv.com/sc/yb/','http://www.sctv.com/sc/zg/','http://www.sctv.com/sc/nj/','http://www.sctv.com/sc/zy/','http://www.sctv.com/sc/sn/','http://www.sctv.com/sc/bz/','http://www.sctv.com/sc/nc/','http://www.sctv.com/sc/gy/','http://www.sctv.com/sc/ls/','http://www.sctv.com/sc/ab/','http://www.sctv.com/sc/ms/','http://www.sctv.com/sc/lz/','http://www.sctv.com/sc/ya/','http://www.sctv.com/sc/gz/','http://www.sctv.com/sc/pzh/','http://www.sctv.com/sc/lsz/','http://www.sctv.com/sc/politics/','http://www.sctv.com/sc/economic/','http://www.sctv.com/sc/live/','http://www.sctv.com/sc/social/','http://www.sctv.com/sc/kjww/','http://www.sctv.com/sc/hlw/']
    count = 0

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="area-left"]//div[@class="list-item"]')

        for node in nodes[:2]:
            date = textify(node.select('.//span[@class="time"]/text()'))
            url = textify(node.select('.//h2/a/@href')).strip('./')
            if '/index_' not in response.url: url = response.url + url
            else:
                _url = response.url.split('/index_')[0]
                url = _url + '/' + url
            _dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            import pdb;pdb.set_trace()
            if _dt_added > get_current_timestamp()-86400*7: yield Request(url,self.details,response)
            else: is_next = False

        nxt_pg = hdoc.select('//div[@class="list-page"]').extract()
        if nxt_pg and is_next:
           self.count += 1
           if 'index' not in response.url: nxt_pg = response.url + 'index_%s.shtml'%self.count
           else: nxt_pg = response.url.split('index')[0] + 'index_%s.shtml'%self.count
           yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="ep-cont"]/h1/text()'))
        dt_added = textify(hdoc.select('//div[@class="ep-time"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=9))
        author = textify(textify(hdoc.select('//div[@class="ep-editor"]/text()')).split(u'\u8d23\u4efb\u7f16\u8f91\uff1a'))
        text = textify(hdoc.select('//div[@id="end-text"]//p//text()'))

        if title:
            print 'url',response.url
            print 'title',xcode(title)
            print 'dt_added',dt_added
            print 'author',xcode(author)
            print 'text',xcode(text)
