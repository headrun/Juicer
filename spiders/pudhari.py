from juicer.utils import *
from dateutil import parser

class PudhariIN(JuicerSpider):

    name = 'pudhari'
    start_urls = ['http://www.pudhari.com/home.aspx']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="main_menu"]//li/a/@href').extract()
        for category in categories[:1]:
            if 'http' not in category: category = 'http://www.pudhari.com' + category
            yield Request(category,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[contains(@id, "ctl00_ContentPlaceHolder1_")]//h4/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.pudhari.com' + link
            #parts = textify(hdoc.select('//h2/parent::div/a[@class="date_line"]/text()')).split('|')
            is_next = True
            nodes = hdoc.select('//div[@class="DateTimeClass"]')

            for node in nodes:
                date = textify(node.select('./text()'))
                dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date < get_current_timestamp()-86400*30:
                    is_next = False
                    continue


'''                yield Request(link,
            if len(parts) > 1:
                date = parts[1]
            else:
                import pdb;pdb.set_trace()


            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))'''
