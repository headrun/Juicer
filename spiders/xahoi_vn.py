from juicer.utils import*
from dateutil import parser
from datetime import datetime
import datetime

class Xahoi_VN(JuicerSpider):
    name = 'xahoi_vn'
    start_urls = ['http://xahoi.com.vn/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[@class="text-title-md2-bold"]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[contains(@class, "tin-noibat-cm")]') or hdoc.select('//div[@class="text-tieudiem-cm"]')
        for node in nodes:
            dt = textify(node.select('.//span[@class="time-title"]//text()'))
            date = ''.join(re.findall('\d{2}/\d{2}/\d{4}', dt))
            date=datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%B %d %Y')
            date_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
            if date_added <  get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//div[@class="pic-noibat-cm fLeft"]/a/@href')) or textify(node.select('.//h2/a/@href'))
            yield Request(link,self.parse_details,response)

        ad_link = textify(hdoc.select('//div[@class="ct-noibat"]//a/@href'))
        yield Request(ad_link,self.parse_details,response)
        
        nxt_pg = textify(hdoc.select('//div[@class="page"]//li/a[contains(text(), "Sau")]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://xahoi.com.vn/' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="tit-chitiet"]//text()'))
        add_txt = textify(hdoc.select('//div[@class="sapo-chitiet"]//text()'))
        txt = textify(hdoc.select('//div[@class="ct-chitiet"]//p[not(img)]//text()'))
        text = add_txt + ' ' + txt
        date = textify(hdoc.select('//span[@class="date"]/text()'))
        dt_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
#        yield item.process()
