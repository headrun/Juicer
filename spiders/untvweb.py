from juicer.utils import*
from dateutil import parser

class Untvweb_PH(JuicerSpider):
    name = 'untvweb'
    start_urls = ['https://www.untvweb.com/news/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@id="menu-header-navigation"]/li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="row bdotted"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="meta"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//a[h3[@class="dark strong"]]/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//div[contains(@class, "next-posts")]/a/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[contains(@class, "np-left")]/h2/text()'))
        text = textify(hdoc.select('//div[@class="entry mbottom2"]//p[not(@class)]//text()'))
        date = textify(hdoc.select('//div[@class="meta"]/p[span[@class="red"]]//following-sibling::text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="meta"]/p/span[@class="red"]/text()'))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author',xcode(author)

    '''
        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','philippines_country_manual'])
        yield item.process()
'''
