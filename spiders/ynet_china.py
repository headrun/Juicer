from juicer.utils import *
from dateutil import parser

class Ynet(JuicerSpider):
    name = "ynet_china"
    start_urls = ['http://www.ynet.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "col_")]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_subcat,response)

    def parse_subcat(self,response):
        hdoc = HTML(response)
        sub_cat = hdoc.select('//ul[@class="cfix fRight"]/li/a/@href').extract() or hdoc.select('//div[contains(@class, "cul_title")]/ul[contains(@class, "cfix")]/li/a/@href').extract()
        for cate in sub_cat:
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li[@class="cfix"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="cfix"]//em[@class="fRight"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added <  get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h2/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="articleTitle"]//h1//text()'))
        date=textify(hdoc.select('//p[@class="sourceBox"]//span[@class="yearMsg"]//text() | //p[@class="sourceBox"]//span[@class="timeMsg"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@id="articleAll"]//p//text()'))
        author = textify(hdoc.select('//span[@class="authors"]//text()'))
        author = author.replace(u'\u8d23\u4efb\u7f16\u8f91\uff1a','')

        print xcode(title)
        print xcode(text)
        print xcode(dt_added)
        print xcode(author)
        import pdb;pdb.set_trace()

