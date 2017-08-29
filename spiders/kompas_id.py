from juicer.utils import*
from dateutil import parser

class Kompas_ID(JuicerSpider):
    name = 'kompas_id'
    start_urls = ['http://www.kompas.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//a[@class="nav__sublink"]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

        add_cat = ['http://kolom.kompas.com/','http://edukasi.kompas.com/']
        for cate in add_cat:
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = textify(hdoc.select('//ul[@class="topic"]/li/a/@href | //div[contains(@class, "kcm-idx-channel")]//div/a/@href') or textify(hdoc.select('//div[@class="kcm-tekno-rubrik rubrik-in clearfix"]//li/a/@href')) or textify(hdoc.select('//ul//li//h3/a/@href | //div[contains(@class, "channel")]//div//a/@href'))
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="kcm-channel-paging mt2 mb2 tcenter"]/ul/li[1]/a[@class="active"]//following::li[1]/a/@href')) or textify(hdoc.select('//ul[@class="paginasi mt2"]/li[@class="active"]//following::li[1]/a/@href'))or textify(hdoc.select('//li[@class="active"]//following::a[1]/@href'))
        if 'http://www.kompasiana.com' in nxt_pg:
            continue
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(Response)
