from juicer.utils import*
from dateutil import parser


class DailypioneerIn(JuicerSpider):
    name = 'dailypioneer'
    start_urls = ['http://www.dailypioneer.com/']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        categories = hdoc.select('//ul[@class="nav clearfix animated"]//a/@href')
        for category in categories:
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@id="most_v_brief"]')
        for node in nodes:
            parts = textify(node.select('.//div[@class="date_time"]/text()')).split('|')
            date = parts[0]
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./h2/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@class="paginate"]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://www.dailypioneer.com/' + nxt_pg
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="news_title"]/a/@href')) or textify(hdoc.select('//h2[@class="news_title"]/text()'))
        text = textify(hdoc.select('//div[@id="left_nav"]//p/text()'))
        parts = textify(hdoc.select('//div[@class="date_time"]/text()')).split('|')
        date = parts[0]
        author = parts[1]
        date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

        item = ITEM(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(date_added))
        item.set('author', {'name':xcode(author)})
        #yield item.process()
