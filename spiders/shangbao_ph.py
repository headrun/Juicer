from juicer.utils import *
from dateutil import parser

class Shangbao(JuicerSpider):
    name = 'shangbao_ph'
    start_urls = ['http://s.shangbao.com.ph/phshangbao_more.php?channel=jjxw','http://s.shangbao.com.ph/phshangbao_more.php?channel=zgsz', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=qwzx', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=lxzx', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=lyzx', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=tzzn', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=gjsx', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=hrxw', 'http://s.shangbao.com.ph/phshangbao_more.php?channel=fgyw']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//a[@target="_blank"]/ancestor::tr')

        for link in links:
            dt = textify(link.select('./td[@class="v12"]/text()'))
            date_added = get_timestamp(parse_date(xcode(dt))-datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            newslink = textify(link.select('./td/a/@href'))
            yield Request(newslink,self.parse_details,response,meta={'dt_added':date_added})

        nxt_uni = u'\u4e0b\u4e00\u9875'
        nxt_pg = textify(hdoc.select('//div[@id="page_bar"]//a[last()]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg:nxt_pg = 'http://s.shangbao.com.ph/' + nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="con_left"]/h1/text()'))
        text = textify(hdoc.select('//div[@class="left_zw"]//text()'))
        dt_added = response.meta['dt_added']
'''
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)'''
