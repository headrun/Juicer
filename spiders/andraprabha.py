from juicer.utils import*
from dateutil import parser

class Prabha_News(JuicerSpider):
    name = 'prabhanews'
    start_urls = ['http://prabhanews.com']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        links = hdoc.select('//li[contains(@id,"menu")]/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="item-details"]/h3')
        for node in nodes:
            date = textify(hdoc.select('.//div[@class="td-post-date"]/text()'))
            dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
            if dt_added < get_current_timestamp()-86400*2:
                is_next = False
                continue
            news_link = textify(hdoc.select('./a/href'))
            if 'http' not in news_link: news_link = 'http://prabhanews.com' + news_link
            yield Request(news_link,self.parse_details,response)

        next_page = textify(hdoc.select('//a[@class="page"]/@href')) 
        if next_page and is_next:
            next_page = 'http://prabhanews.com' + next_page
            yield Request(next_page,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="entry-title"]/text()'))
        text = textify(hdoc.select('//div[@class="td-post-content"]//p/text()'))
        date = textify(hdoc.select('//div[@class="td_data_time"]/text()'))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minute=30))

        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)



