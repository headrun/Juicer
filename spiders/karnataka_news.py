from juicer.utils import*
from dateutil import parser

class KarnatakaNews(JuicerSpider):
    name = 'karnataka_news'
    start_urls = ['http://www.newskarnataka.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav navbar-nav "]//li/a[@title]//@href').extract()
        for cat in categories:
            if 'a.com/top-news' in cat or 'ka.com/bangalore' in cat or 'nataka.com/mysore' in cat or 'nataka.com/mangalore' in cat or '.com/udupi' in cat or 'om/other-cities' in cat:
                continue
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        more_link = textify(hdoc.select('//div[@class="read"]//a/@href'))
        if 'http' not in more_link: more_link = 'http://www.newskarnataka.com/' + more_link
        yield Request(more_link,self.parse_main_links,response)

    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="category_news_section news_conatiner_border"]')
        for node in nodes:
            date  = textify(node.select('.//a[i[@class="fa fa-clock-o"]]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) -datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a[@title]/@href'))
            if 'http' not in link: link = 'http://www.newskarnataka.com/' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//a[@rel="next"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.newskarnataka.com/' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="innrpg_title"]//text()'))
        date = textify(hdoc.select('//span[@class="fa fa-calendar"]//following-sibling::text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) -datetime.timedelta(hours=5,minutes=30))
        text = textify(hdoc.select('//div[@class="news_detail"]//p//text()'))
        author = textify(hdoc.select('//a[@title="Published By"]/text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
