from juicer.utils import*
from dateutil import parser

class MangloreanNews(JuicerSpider):
    name = 'manglorean_news'
    start_urls = ['http://www.mangalorean.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@id="td-header-menu"]//a[contains(@href,"category")]/@href').extract()
        for category in categories:
                yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="item-details"]')
        for node in nodes:
            link = textify(node.select('./h3/a/@href'))
            date = textify(node.select('.//span[@class="td-post-date"]//text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./h3/a/@href'))
            yield Request(link,self.parse_details,response)

            next_page =  hdoc.select('//div[@class="page-nav td-pb-padding-side"]/a/@href').extract()
            if next_page and is_next:
                next_page = next_page[-1]
                yield Request(next_page,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="entry-title"]/text()'))
   #    text = textify(hdoc.select('//div[@class="td-post-content"]/h3/strong[not(contains(text(),"Related News:"))]/text() | //p[@style="txt-align: justify;"]//text() | //div[@style="text-align: justify;"]//text()'))
        text = textify(hdoc.select('//div[@class="td-post-content"]/h3/strong[not(contains(text(),"Related News:"))]/text()')) + textify(hdoc.select('//div[@class="td-post-content"]//p//text()'))
        author = textify(hdoc.select('//div[@class="td-post-author-name"]//text()')).split(',')[0].replace('By','')
        date = textify(hdoc.select('//span[@class="td-post-date"]//text()'))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'date',xcode(date)
