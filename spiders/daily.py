from juicer.utils import*
from dateutil import parser

class DailyExpress(JuicerSpider):
    name = 'dailyexpress'
    start_urls = ['http://dailyexpress.com.my/local.cfm','http://dailyexpress.com.my/national.cfm','http://dailyexpress.com.my/business.cfm','http://dailyexpress.com.my/sport.cfm','http://dailyexpress.com.my/features.cfm']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="headlines"]/@onclick').extract()
        if 'http' not in links:
            links = 'http://www.dailyexpress.com.my/' + str(links.split('location=')[-1]).strip("';")
            yield Request(links,self.parse,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="headlines"]//div[@class="title"]/text()'))
        date = textify(hdoc.select('//div[contains(text(),"Published on:")]/text()')).split(':')[-1]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="headlines"]/text() | //div[@class="headlines"]/b/text() |//div[@class="headlines"]/p//text    ()'))

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'dt_added', xcode(dt_added)


