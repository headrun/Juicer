from juicer.utils import *
from dateutil import parser
import goslate

class AajkaalIN(JuicerSpider):
    name = 'aajkaal'
    start_urls = ['http://www.aajkaal.in/']
#    start_urls = ['http://www.aajkaal.in/', 'http://www.aajkaal.in/enewspaper/sambad/28','http://www.aajkaal.in/enewspaper/sambad/14', 'http://www.aajkaal.in/enewspaper/sambad/27', 'http://www.aajkaal.in/enewspaper/sambad/29']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav navbar-nav pull-right"]//li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

        ext_categories = ['http://www.aajkaal.in/sciencetechnology','http://www.aajkaal.in/helth']
        for cate in ext_categories:
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="text-box"]/h3/a/@href').extract()
        for link in nodes:
            #link = 'http://www.aajkaal.in/news/kolkata/jaganath-ghat--phool-market-0ql2'
            #link = 'http://www.aajkaal.in/news/business/silver-pompano-piciculture-eab9'
            yield Request(link,self.parse_details)

        nxt_pg = textify(hdoc.select('//ul[@class="cat-pagination pagination"]//li/a[@aria-label="Next"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="col-md-12"]//h1//text()'))
        dt=textify(hdoc.select('//div[@class="col-md-12"]//ul//li[i[@class="fa fa-pencil-square-o"]]/preceding-sibling::li[i[@class="fa fa-calendar"]]//text()'))
        gs = goslate.Goslate()
        date = gs.translate(dt, 'en')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        text = textify(hdoc.select('//div[@class="blog-detail "]//p[@class="margin-top-bottom-10px"]//text()'))
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace()
