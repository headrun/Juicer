from juicer.utils import*
from dateutil import parser

class Gulte_IN(JuicerSpider):
    name = 'gulte_in'
    start_urls = ['http://telugu.gulte.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "menu")]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)
        eng_categories = ['http://www.gulte.com/movienews','http://www.gulte.com/news','http://www.gulte.com/photos','http://www.gulte.com/videos','http://www.gulte.com/moviereviews','http://www.gulte.com/pressrelease','http://www.gulte.com/overseas','http://www.gulte.com/lifestyle']
        for cate in eng_categories:
            yield Request(cate,self.parse_links,response)
    
    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="txt"]')
        for node in nodes:
            date = textify(node.select('.//code[not(contains(@class, "shares"))]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            links = textify(node.select('./strong/a/@href'))
            yield Request(links,self.parse_details,response)

        if not nodes:
            add_links = hdoc.select('//ul[@class="reviews_thumb"]//li/a/@href').extract()
            for link in add_links:
                yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagination"]//a[@title="Next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc =HTML(response)
        title = textify(hdoc.select('//div[@class="article"]//h2//text()')) or textify(hdoc.select('//div[@class="article"]//h1//text()')) or textify(hdoc.select('//div[@class="movie_title"]//h1//text()'))

        date=textify(hdoc.select('//div[@class="links"]//code[not(contains(@class, "shares"))]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        text = textify(hdoc.select('//div[@class="content"]//p//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()


