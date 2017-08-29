from juicer.utils import *
from dateutil import parser

class  MobileWorld(JuicerSpider):
    name = "mobile_world_my"
    start_urls = ['http://www.mobileworld.my/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@id="masonry"]//div[@class="content-space"]')
        import pdb;pdb.set_trace()
        for node in nodes:
            url = node.select('.//div[@class="post-title"]/a/@href').extract()
            date = textify(node.select('.//div[@class="date"]//span[1]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added <  get_current_timestamp()-86400*180:
                is_next = False
                continue

            if "http:" not in url: url = 'http://www.mobileworld.my/'+textify(url)
            yield Request(url,self.parse_details,response)

        nxt_page = hdoc.select('//div[@class="font2 pagination"]/a[@class="selected"]/following-sibling::a[1]/text()').extract()
        if nxt_page and is_next:
            nxt_pgurl = 'http://www.mobileworld.my/?&pg=' + textify(nxt_page)
            yield Request(nxt_pgurl,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="content"]//h1/text()')[0])
        text = textify(hdoc.select('//div[@id="content"]//div[@id="pg-content"]//text()'))
        dt_added = textify(hdoc.select('//div[@id="content"]//div[@class="page-date"]/span[1]/text()'))
        author = textify(hdoc.select('//div[@id="content"]//div[@class="page-date"]/a[@rel="author"]/text()'))
        author_ref_url = textify(hdoc.select('//div[@id="content"]//div[@class="page-date"]/a[@rel="author"]/@href'))
        author = {'name':author,'url':author_ref_url}
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author',xcode(author)
'''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author', author)
        item.set('url', response.url)
        #yield item.process() '''
