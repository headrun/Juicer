from juicer.utils import *

class DailySun(JuicerSpider):
    name = 'daily_sun'
    start_urls = ['http://www.daily-sun.com']

    def parse(self,response):
        hdoc = HTML(response)
        cat_urls = hdoc.select('//div[@class="tab-content"]/div[@role="tabpanel"]//li/a/@href').extract()
        for caturls in cat_urls[:2]:
            if 'http' not in caturls:caturls = 'http://www.daily-sun.com/' + caturls.strip('.')
            yield Request(caturls,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        news_links = hdoc.select('//div[@class="row-fluid"]//div[@id]/a/@href').extract() or hdoc.select('//div[@class="row-fluid"]//div[@class]/h4/a/@href').extract()
        for news_link in news_links:
            if 'http' not in news_link:news_link = 'http://www.daily-sun.com' + news_link.strip('.')
            yield Request(news_link,self.details,response)

        nxt_pg = textify(hdoc.select('//div[@class="paginatorcustom"]/a[contains(text(),">")]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id]/h2//text()'))
        date = textify(hdoc.select('//div[@class="dtlDate"]/span/text()'))
        author = textify(hdoc.select('//div[@id="hl3"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@id="myText"]//p//text()'))
        import pdb;pdb.set_trace()

'''        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('author',{'name':xcode(author)})
        item.set('text',xcode(text))
        yield item.process()'''
