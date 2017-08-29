from juicer.utils import *
from dateutil import parser

class DailyexpressMalaysia(JuicerSpider):
    name = 'dailyexpress_my'
    start_urls = ['http://www.dailyexpress.com.my/features.cfm','http://www.dailyexpress.com.my/local.cfm','http://www.dailyexpress.com.my/national.cfm','http://www.dailyexpress.com.my/business.cfm','http://www.dailyexpress.com.my/sport.cfm']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False


    def parse(self,response):
        hdoc = HTML(response)
        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        links = hdoc.select('//div[@class="headlines"]/@onclick').extract()
        for link in links:
            link = 'http://www.dailyexpress.com.my/' + str(link.split('location=')[-1]).strip("';")
            yield Request(link,self.details,response)

    def details(self,response):
        hdoc  = HTML(response)
        title = textify(hdoc.select('//div[@class="headlines"]//div[@class="title"]/text()'))
        date = textify(hdoc.select('//div[contains(text(),"Published on:")]/text()')).split(':')[-1]
       #dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="headlines"]/text() | //div[@class="headlines"]/b/text() |//div[@class="headlines"]/p//text()'))

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'date', xcode(date)

    ''' item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        yield item.process()'''
