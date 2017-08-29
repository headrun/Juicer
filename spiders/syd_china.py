from juicer.utils import *
from dateutil import parser

class SydChina(JuicerSpider):
    name = "syd_china"
    start_urls = ['http://news.syd.com.cn/', 'http://caijing.syd.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        main_links = hdoc.select('//div[@class="more"]/a/@href | //a[contains(.,"%s")]/@href'%u'\u66f4\u591a>>').extract() or hdoc.select('//div[contains(@class, "class_m_l2_r")]/a/@href').extract()
        for link in main_links:
            yield Request(link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//li/a/@href').extract()
        for link in nodes:
            if 'video.syd.com.cn' in link:
                continue
            yield Request(link,self.parse_details,response)


        nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="new_title"]//text()'))
        text = textify(hdoc.select('//div[@class="new_content"]//p//text()'))
        dt = textify(hdoc.select('//div[@class="new_sour"]//text()'))
        date = ''.join(re.findall('\d{4}-\d{2}-\d{2}',dt))
        dt_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="ns_down"]//text()'))
        author = author.replace(u'\u7f16\u8f91\uff1a','')

        if title == '' or text == '' or dt == '':
            import pdb;pdb.set_trace()

        """
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()
"""
