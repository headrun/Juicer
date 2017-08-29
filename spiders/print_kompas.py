from juicer.utils import *
from dateutil import parser

class PrintKompas(JuicerSpider):
    name = 'print_kompas'
    start_urls = ['http://print.kompas.com/rubrik/b1/politik?p=1&ps=50']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//articel[@class="article-main pr"] | //div[@class="cf"]/section[contains(@class,"sections")]')

        for node in nodes:
            date = node.select('.//time[@datetime]/text()')
            news_link = node.select('.//h3[@class="article-title"]/a/@href')
            if 'http' not in news_link: news_link = 'http://print.kompas.com' + news_link
            yield Request(news_link,self.parse_details,response)

        nxt_pg = hdoc.select('//li[@class="page-nav next"]/a/@href')
        if nxt_pg:
            if 'http' not in nxt_pg: nxt_pg = 'http://print.kompas.com' + nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)

