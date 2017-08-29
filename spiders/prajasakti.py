from juicer.utils import *
from dateutil import parser

class Prajasakti(JuicerSpider):
    name = 'prajasakti'
    start_urls=['http://www.prajasakti.com/']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        links = hdoc.select('//ul[@id="mainmenu"]/li//a/@href').extract()
        for link in links:
            import pdb;pdb.set_trace()
            if 'http' not in link:link = 'http://www.prajasakti.com' + link
            yield Request(link,self.parse_articles,response)

    def parse_articles(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="rightcontp"]')
        for node in nodes:
            date = textify(node.select('./div[@class="post-meta"]//text()'))
            date_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
            if date_added < get_current_timestamp()-86400*7:
                import pdb;pdb.set_trace()
                is_next = False
                continue
            news_link = textify(node.select('./h2/a/@href'))
            news_link = 'http://www.prajasakti.com/Article/TaajaVarthalu/1846030'
            import pdb;pdb.set_trace()
            yield Request(news_link,self.details,response)

        nxt_pg = hdoc.select('//li[@class="next"]/a/@href').extract()
        if nxt_pg and is_next:
            nxt_pg = 'http://www.prajasakti.com' + nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//h1/a[@title]/text()'))
        dt = textify(hdoc.select('//div/p[contains(text(),"Posted On")]/text()')).split('Posted On')[-1]
        dt_added = get_timestamp(parse_date(dt))
        text = textify(hdoc.select('//a[@title]/parent::h1/following-sibling::p//text()'))
'''
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        #yield item.process()'''
