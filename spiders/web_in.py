from juicer.utils import*
from dateutil import parser

class WebIndia(JuicerSpider):
    name = 'web_india'
    start_urls = ['http://news.webindia123.com/news/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="long-menu"]//a[@id="top"]/@href').extract()
        for category in categories:
            if 'http' not in category: category = 'http://news.webindia123.com' + category
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//table[@width="100%"]//td[@valign="top"]')
        for node in nodes:
            date = textify(node.select('.//td[@height="25"]/div/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30)
            if dt_added < get_current_timestamp()-86400*30
                is_next = False
                continue
            link = textify(node.select('.//a/@href'))
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="head_line"]/text()'))
        text = textify(hdoc.select('//'))
