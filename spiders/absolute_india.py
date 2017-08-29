from juicer.utils import *
from dateutil import parser

class AbsoluteIndia(JuicerSpider):
    name = "absolute_india"
    start_urls = ['http://absoluteindianews.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//nav[@id="site-navigation"]//ul[@class="sub-menu"]/preceding-sibling::a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//article[contains(@id, "post-")]')
        for node in nodes:  
            date = textify(node.select('.//time[@class="entry-date published"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h2[@class="entry-title"]/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="nav-previous"]/a/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

    """
    start_urls = ['http://www.absoluteindianews.com/section.php?id=1','http://www.absoluteindianews.com/section.php?id=2','http://www.absoluteindianews.com/section.php?id=6','http://www.absoluteindianews.com/section.php?id=3','http://www.absoluteindianews.com/section.php?id=5','http://www.absoluteindianews.com/section.php?id=26']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="article-story"]//div[@class="wrapper2"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="storymatter"]/b/text()'))
        text = textify(hdoc.select('//div[@class="storymatter"]//p//text()'))

        item =Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set('url', response.url)
        yield item.process()
"""
