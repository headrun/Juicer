from juicer.utils import *
from dateutil import parser

class MangloreanTimes(JuicerSpider):
    name = "manglorean_times"
    start_urls = ['http://www.mangalorean.com/']

    def parse(self,response):
        hdoc = HTML(response)
        category_urls = hdoc.select('//div[@id="td-header-menu"]//a[contains(@href, "/category/")]/@href').extract()
        for category in category_urls:
            yield Request(category,self.parse_category,response)

    def parse_category(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="td-ss-main-content"]//div[@class="item-details"]')
        for node in nodes:
            date = textify(node.select('.//span//text()')).split('-')[-1]
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./h3/a/@href').extract())
            yield Request(link,self.parse_next,response)
        import pdb;pdb.set_trace()
        next_page =  hdoc.select('//div[@class="page-nav td-pb-padding-side"]/a/@href').extract()
        if next_page and is_next:
            next_page = next_page[-1]
            yield Request(next_page,self.parse_category)


    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="entry-title"]'))
        text = textify(hdoc.select('//div[@class="td-post-content"]/h3/strong[not(contains(text(),"Related News:"))]/text() | //div[@class="td-post-content"]//p//text() '))
        author = textify(hdoc.select('//meta[@name="author"]/@content')).split(',')[0]
        author_url = textify(hdoc.select('//div[@class="td-post-author-name"]/a/@href'))
        date = textify(hdoc.select('//header[@class="td-post-title"]//time/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('author',{'name':xcode(author), 'url':author_url})
        item.set('dt_added', dt_added)
