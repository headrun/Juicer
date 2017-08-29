from juicer.utils import *
from dateutil import parser

class NewsAbahtimes(JuicerSpider):
    name = 'newsabahtimes_my'
    start_urls = ['http://www.newsabahtimes.com.my/nstweb/category/Business','http://www.newsabahtimes.com.my/nstweb/category/Local','http://www.newsabahtimes.com.my/nstweb/category/Foreign','http://www.newsabahtimes.com.my/nstweb/category/Sports','http://www.newsabahtimes.com.my/nstweb/category/Leisure','http://www.newsabahtimes.com.my/nstweb/category/BM','http://www.newsabahtimes.com.my/nstweb/category/Kadazan+Dusun','http://www.newsabahtimes.com.my/nstweb/archives']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//span[@class="article-title"]/a/@href').extract()
        links = 'http://www.newsabahtimes.com.my/nstweb/fullstory/9788'
        yield Request(links,self.parse_details,response)

        nxt_page = textify(hdoc.select('//a[contains(text(),"Next page")]/@href'))
        if 'http' not in nxt_page:
            nxt_page = 'http://www.newsabahtimes.com.my' + nxt_page
            yield Request(nxt_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//h1[@class="title"]/text()'))
        date = textify(hdoc.select('//span[@class="picture-title"]//text()'))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//span[@class="picture-title"]/parent::td/p//text()'))
        import pdb;pdb.set_trace()

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'date',xcode(date)
        '''
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('date',dt_added)
        item.set('text',xcode(text))'''
