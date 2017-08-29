from juicer.utils import *
from dateutil import parser

class Hket(JuicerSpider):
    name = 'hket_hk'
    start_urls = ['http://inews.hket.com/sran001/%E5%85%A8%E9%83%A8']

    def parse(self,response):
        hdoc = HTML(response)
        date = textify(hdoc.select('//option[@selected="selected"]/text()'))
        links = hdoc.select('//table[@id="eti-inews-list"]/tr')
        for link in links:
            dt =  date + ' ' + textify(link.select('./td/span/text()'))
            newstitle = textify(link.select('.//a[@title]/text()'))
            newslink = textify(link.select('.//a[@title]/@href'))
            newslink = 'http://inews.hket.com/article/1497651/%E6%96%B0%E7%95%8C%E4%BA%8C%E6%89%8B%E6%88%90%E4%BA%A4%E4%B8%80%E8%A6%BD'
            yield Request(newslink,self.details,response,meta={'title':newstitle,'dt_added':dt})

        nxt_pg = hdoc.select('//div[@id="eti-article-content"]/a/@href').extract()
        if nxt_pg:
            try:nxt_pg = nxt_pg[0]
            except: nxt_pg = nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = response.meta['title']
        dt_added = response.meta['dt_added']
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@id="content-main"]/p//text()')) or textify(hdoc.select('//div[@class="content-content"]/p//text()'))
        if text == '':
            text = textify(hdoc.select('//div[@class="content"]/p//text()')) or textify(hdoc.select('//div[@id="eti-article-content-body"]/p//text()'))
        if text == '':import pdb;pdb.set_trace()
        import pdb;pdb.set_trace()
        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'dt_added',dt_added
        print 'text',xcode(text)
