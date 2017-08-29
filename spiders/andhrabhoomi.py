from juicer.utils import *
from dateutil import parser

class Andhrabhoomi(JuicerSpider):
    name = 'andhrabhoomi_news'
    start_urls = ['http://www.andhrabhoomi.net/nation','http://www.andhrabhoomi.net/category/135','http://www.andhrabhoomi.net/state','http://www.andhrabhoomi.net/andhrapradesh','http://www.andhrabhoomi.net/telangana','http://www.andhrabhoomi.net/taxonomylistingbyparent/10','http://www.andhrabhoomi.net/sports','http://www.andhrabhoomi.net/business','http://www.andhrabhoomi.net/category/15','http://www.andhrabhoomi.net/category/16','http://www.andhrabhoomi.net/category/17','http://www.andhrabhoomi.net/category/18','http://www.andhrabhoomi.net/category/19','http://www.andhrabhoomi.net/category/20','http://www.andhrabhoomi.net/category/133','http://www.andhrabhoomi.net/category/22','http://www.andhrabhoomi.net/category/23','http://www.andhrabhoomi.net/category/24','http://www.andhrabhoomi.net/category/25','http://www.andhrabhoomi.net/daily_features/chitra','http://www.andhrabhoomi.net/weekly_features/akshara','http://www.andhrabhoomi.net/category/66','http://www.andhrabhoomi.net/category/67','http://www.andhrabhoomi.net/category/69','http://www.andhrabhoomi.net/category/68','http://www.andhrabhoomi.net/category/134','http://www.andhrabhoomi.net/weekly_features/sahithi','http://www.andhrabhoomi.net/weekly_features/yuva','http://www.andhrabhoomi.net/weekly_features/sanjeevani','http://www.andhrabhoomi.net/weekly_features/focus','http://www.andhrabhoomi.net/weekly_features/aatapoti','http://www.andhrabhoomi.net/weekly_features/weakpoint','http://www.andhrabhoomi.net/merupu/uttara_telangana','http://www.andhrabhoomi.net/category/132','http://www.andhrabhoomi.net/merupu/nellore','http://www.andhrabhoomi.net/merupu/rajahmundry','http://www.andhrabhoomi.net/merupu/vijayawada','http://www.andhrabhoomi.net/merupu/visakhapatnam','http://www.andhrabhoomi.net/weekly_special/aadivaram_listing/42','http://www.andhrabhoomi.net/weekly_special/vennala_listing/29']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//div[@class="view-content"]/div[contains(@class,"views-row")]')
        for link in links:
            date = textify(link.select('./div[contains(@class,"views-field-changed")]/span/text()'))
            date_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            news_link = textify(link.select('./div[contains(@class,"views-field-title")]/span/a/@href'))
            if 'http' not in news_link: news_link= 'http://www.andhrabhoomi.net' + news_link
            yield Request(news_link,self.details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.andhrabhoomi.net' + nxt_pg
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse,response)
    
    
    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="page-title"]/text()'))
        dt = textify(hdoc.select('//span[@class="submitted"]/span/text()'))
        dt_added = get_timestamp(parse_date(dt) - datetime.timedelta(hours=5, minutes=30))
        text = textify(hdoc.select('//div[@property="content:encoded"]'))
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()


