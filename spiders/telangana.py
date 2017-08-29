from juicer.utils import*
from dateutil import parser

class Telangana(JuicerSpider):
    name = 'telangana'    
    start_urls = ['https://www.telangana99.com/']

    def parse(self,response):
        hdoc = HTML(response)
        catgories = hdoc.select('//div[@class="top_navi"]//li/a/@href')
        print categories
        for category in categories[:2]:
            print category
            import pdb;pdb.set_trace()
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="list_new"]/ul/li/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'https://www.telangana99.com' + link
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="innerbodybg"]//h1/text()'))
        text = textify(hdoc.select('//div[@class="description"]//span/text()'))
        date = textify(hdoc.select('//div[@class="innerbodybg"]//div[@align="right"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))


