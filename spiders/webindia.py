from juicer.utils import*
from dateutil import parser

class WebIndia(JuicerSpider):
    name = 'webindia'
    start_urls = ['http://www.webindia123.com/']

    def parse(self,response):
        hdoc = HTML(response)
        category = textify(hdoc.select('//td[@align="center"]//a[@id="top"]/@href'))
        for link in category:
            if 'http' not in link
                link = 'http://news.webindia123.com/news/index.html' + link
                yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        urls = textify(hdoc.select('//tr//td[@valign="top"]//a[@id="head"]/@href'))
        for url in urls:
            if 'http' not in url
                url = 'http://news.webindia123.com/news/index.html' + url
                yield Request(url,self.parse_final,response)

    def parse_final(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="head_line"]//text()'))
        text = textify(hdoc.select)
