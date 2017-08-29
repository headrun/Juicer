from juicer.utils import *
from dateutil import parser

class UfhnewsIN(JuicerSpider):
    name = 'ufhnews'
    start_urls = ['http://www.ufhnews.in/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@id="nav"]//a/@href').extract()
        for category in categories[:2]:
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[contains(@class, "col-md-4")]//a/@href').extract()
        for link in links:
            import pdb;pdb.set_trace()
            if 'amit.misrag.com/app' in link:
                continue
        #date = textify(hdoc.select('//div[@class="btn btn-danger"]//text()'))
        #dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        #if date_added < get_current_timestamp()-86400*30:
         #   continue
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
       # title = textify(hdoc.select('//div[@class="col-md-12"]/h1//text()'))
        date = textify(hdoc.select('//div[@class="btn btn-danger"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        if date_added < get_current_timestamp()-86400*30:
            continue
        title = textify(hdoc.select('//div[@class="col-md-12"]/h1//text()'))
        text = textify(hdoc.select('//div[@class="pull-right"]/following-sibling::p/text()'))
        author = textify(hdoc.select('//div[@class="btn btn-default"]//text()')).split(',')[0]
        import pdb;pdb.set_trace()

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'dt_added', xcode(dt_added)
        print 'author', xcode(author)
