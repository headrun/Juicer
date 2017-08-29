from juicer.utils import *
from dateutil import parser

class Prajasakthi_n(JuicerSpider):
    name = 'prajasakti_n'
    start_urls = ['http://www.prajasakti.com/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//li[contains(@class, "menu-item")]/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.prajasakti.com' + link
            if 'epaper' in link or 'CartoonSect' in link:
                continue
            yield Request(link,self.parse_articles,response)


    def parse_articles(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="bp-entry"]')
        for node in nodes:
            date = textify(node.select('.//div[contains(@class, "post-meta")]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            news_link = textify(node.select('.//h3/a/@href'))
            if 'http' not in news_link: news_link = 'http://www.prajasakti.com' + news_link
            yield Request(news_link,self.parse_details,response)

        next_pg = textify(hdoc.select('//a[@class="next"]/@href'))
        if 'http' not in next_pg: next_pg = 'http://www.prajasakti.com' + next_pg
        if next_pg and is_next:
            yield Request(next_pg,self.parse_articles,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="post-tile entry-title"]/text()')) or hdoc.select('//div[@class="entry-content"]/p/strong/text()').extract()[0]
        text = textify(hdoc.select('//div[@class="entry-content"]/p//text()'))
        date = textify(hdoc.select('//span[@class="author vcard"]/time/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace()
