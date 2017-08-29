from juicer.utils import *
from dateutil import parser

class Ahmedabadmirror(JuicerSpider):
    name = 'ahmedabadmirror'
    start_urls = ['http://www.ahmedabadmirror.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//a[@class="sublink"]/@href').extract()
        for category in categories[:1]:
            if 'http' not in category:
                category = 'http://www.ahmedabadmirror.com' + category
                yield Request(category,self.parse_details,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@id="content"]//h4/a/@href').extract()
        for link in links[:1]:
            if 'http' not in link: link = 'http://www.ahmedabadmirror.com' + link
            yield Request(link,self.parse_finaldetails,response)
        nxt_pg = textify(hdoc.select('//div[contains(@style, "float:")]/a/@href'))
        if 'http' not in nxt_pg and nxt_pg: nxt_pg = 'http://www.ahmedabadmirror.com' + nxt_pg
        yield Request(nxt_pg,self.parse_details,response)


    def parse_finaldetails(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//div[@class="heading2"]/h1/text()'))
        text = textify(hdoc.select('//div[@class="Normal"]/text()'))
        author = textify(hdoc.select('//span[@id="authortext"]/text()'))
        auth_date = hdoc.select('//span[@style="font-size:9px;"]/parent::span/text()').extract()
        if author == '' and auth_date != '':
            author = ''.join(auth_date[:-1])
        if auth_date:date = auth_date[-1]
        else:date = textify(hdoc.select('//span[@class="byline"]/text()'))
      # dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))


        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'date',xcode(date)
'''
        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author', {'name':xcode(author)}) '''
