from juicer.utils import*
from dateutil import parser

class AdelaidAu(JuicerSpider):
    name = 'adelaidenow'
    start_urls = ['http://www.adelaidenow.com.au/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [302]

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//ul[@class="nav-list tier-1"]/li/a/@href').extract()
        for link in links[:2]:
            if 'http' not in link:link = 'http://www.adelaidenow.com.au' + link
            print link
            yield Request(link, self.parse_details, meta={'dont_redirect':True})

    def parse_details(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[contains(@class, "story-block")]/h4[@class="heading"]/a/@href').extract()
        import pdb;pdb.set_trace()
        for url in urls:
            #if 'http' not in url: url = 'http://www.adelaidenow.com.au' + url
            yield Request(url, self.parse_self_details, meta={'dont_redirect':True,'handle_httpstatus_list':[302]})

    '''def parse_self_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="story-header_title"]/text()'))
        text = textify(hdoc.select('//article[@class="story-content"]//p//text()'))
        date = textify(hdoc.select('//div[@class="story-header non_premium"]//time//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'dt_added', xcode(dt_added)'''
