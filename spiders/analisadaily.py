from juicer.utils import*
from dateutil import parser

class Analisadaily(JuicerSpider):
    name = 'analisadaily'
    start_urls = ['http://news.analisadaily.com/','http://sepakbola.analisadaily.com/','http://sport.analisadaily.com/','http://tekno.analisadaily.com/','http://entertainment.analisadaily.com/','http://lifestyle.analisadaily.com/','http://ragam.analisadaily.com/']

    def parse(self,response):
        hdoc = HTML(response)
        links =  hdoc.select('//div[@id="titles"]/a/@href').extract()
        for link in links[:4]:
            yield Request(link,self.parse_details,response)
        next_page = hdoc.select('//a[@rel="next"]/@href').extract()
        if next_page:
            next_p = next_page[0]
            yield Request(next_p,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="article yoyo col col-md-8 col-sm-7"]/h3/text()'))
        text = textify(hdoc.select('//div[@class="chatNews"]//p[not(contains(@class, "date")) and not(contains(@class, "small")) and not(contains(text(), "Tags :"))]//text()'))
        date = textify(hdoc.select('//p[@class="dateNews"]/text()').extract()).split(',')[-1].strip()
        month = str(date.strip().split(' ')[1])
        s = {'Januari':'January','Februari':'February','Maret':'March','April':'April','Mei':'May','Juni':'June','Juli':'July','Augustus':'August','September':'September','Oktober':'October','Nopember':'November','Desember':'December'}
        for key,value in s.iteritems():
            if key in month:
                eng_month = value
                date = date.replace(month,eng_month)
                dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))

        print '/n'
        print response.url
        print 'title' ,xcode(title)
        print 'text' ,xcode(text)
        print 'dt_added' ,xcode(dt_added)

