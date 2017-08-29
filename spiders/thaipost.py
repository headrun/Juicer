from juicer.utils import*
from dateutil import parser

class Thaipost(JuicerSpider):
    name = 'thaipost'
    start_urls = ['http://www.thaipost.net/?q=focusonline', 'http://www.thaipost.net/?q=plew.seengern','http://www.thaipost.net/?q=politics','http://www.thaipost.net/?q=editor','http://www.thaipost.net/?q=xcide','http://www.thaipost.net/?q=economy','http://www.thaipost.net/?q=khunnoy','http://www.thaipost.net/?q=oversea','http://www.thaipost.net/?q=reading','http://www.thaipost.net/?q=%E0%B9%81%E0%B8%97%E0%B8%9A%E0%B8%A5%E0%B8%AD%E0%B8%A2%E0%B8%94%E0%B9%8C','http://www.thaipost.net/?q=newsupdate','http://www.thaipost.net/?q=krajokraingow','http://www.thaipost.net/?q=sport','http://www.thaipost.net/?q=kunparkyahklao','http://www.thaipost.net/?q=eduhealth','http://www.thaipost.net/?q=memopage4','http://www.thaipost.net/?q=inside','http://www.thaipost.net/?q=%E0%B8%9A%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%97%E0%B8%B4%E0%B8%87','http://www.thaipost.net/?q=travel','http://www.thaipost.net/?q=%E0%B8%AA%E0%B8%B8%E0%B8%82%E0%B8%A0%E0%B8%B2%E0%B8%A7%E0%B8%B0...%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B9%84%E0%B8%94%E0%B9%89','http://www.thaipost.net/?q=%E0%B8%AD%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%A3','http://www.thaipost.net/?q=ecofocus','http://www.thaipost.net/?q=motoring','http://www.thaipost.net/?q=%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B9%80%E0%B8%A8%E0%B8%A9']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="tm_category_box"]')
        for node in nodes:
            date = textify(node.select('.//div[i[@class="fa fa-calendar"]]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) -  datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//a[@rel="bookmark"]/@href')) 
            if 'http' not in link: link = 'http://www.thaipost.net' + link
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//ul[@class="pager"]//a[@title="Go to next page"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.thaipost.net' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)
    
    def parse_details(self,response):
        hdoc=HTML(response)
        title = textify(hdoc.select('//div[@class="tm_cat_metatitle"]/h1//text()'))
        date = textify(hdoc.select('//div[i[@class="fa fa-calendar"]]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
        text = textify(hdoc.select('//div[@class="field-item even"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','thailand_country_manual'])
        yield item.process()


