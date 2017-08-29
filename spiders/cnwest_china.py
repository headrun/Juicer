from juicer.utils import *
from dateutil import parser

class Cnwest(JuicerSpider):
    name = "cnwest_china"
    start_urls = ['http://news.cnwest.com/node_4973.htm','http://news.cnwest.com/node_59046.htm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list"]//a[contains(@href,"content/")]//@href').extract()
        for link in urls:
            if 'http' not in link: link = 'http://news.cnwest.com/' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@id="displaypagenum"]//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if 'http' not in nxt_pg: nxt_pg=  'http://news.cnwest.com/' + nxt_pg
        if nxt_pg:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="layout"]//h1//text()')) or textify(hdoc.select('//div[@id="title"]//h4//text()'))
        text = textify(hdoc.select('//div[@class="con-detail"]//p//text()')) or textify(hdoc.select('//div[@id="content"]//p//text()')) 
        junk_txt = textify(hdoc.select('//p[@class="bianji"]//text()'))
        text= text.replace(junk_txt,'')
        dat = textify(hdoc.select('//div[@class="layout-left"]/p[contains(.,"%s")]/text()'%u'\u65f6\u95f4')) or textify(hdoc.select('//div[@id="title"]//span//text()'))

        date = ''.join(re.findall(".*-.*-.*-?",dat))
        dt_added = get_timestamp(parse_date(xcode(date))- datetime.timedelta(hours=8))


        
        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        #yield item.process()
