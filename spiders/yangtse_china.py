from juicer.utils import *
from dateutil import parser

class Yangtse(JuicerSpider):
    name = "yangtse_china"
    start_urls = ['http://www.yangtse.com/jiangsu/','http://www.yangtse.com/nanjing/','http://www.yangtse.com/shehui/','http://www.yangtse.com/jiaoyu/','http://www.yangtse.com/wenyu/','http://www.yangtse.com/tiyu/','http://www.yangtse.com/guonei/','http://www.yangtse.com/guoji/','http://www.yangtse.com/caijing/','http://www.yangtse.com/caijing/','http://www.yangtse.com/jiankang/','http://www.yangtse.com/keji/','http://www.yangtse.com/shishang/','http://www.yangtse.com/yangzijiancang/','http://www.yangtse.com/qiche/','http://www.yangtse.com/meishi/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[contains(@class, "leftcon")]')
        for node in nodes:
            date = textify(node.select('.//span[@class="info2"]//text()'))
            date_added=  get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h2[@class="tit"]/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="content_title"]//span//text()'))
        text = textify(hdoc.select('//div[@id="article"]//p//text()')) 
        date=textify(hdoc.select('//div[@id="time"]//text()'))
        date = ''.join(re.findall('\d{4}-\d{2}-\d{2}',date))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        
        
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()
