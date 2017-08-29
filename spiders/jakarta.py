from juicer.utils import*
from dateutil import parser

class jakarta(JuicerSpider):
    name = 'jakarta'
    start_urls = ['http://pusat.jakarta.go.id/?mod=main&sub=info&action=news_list', 'http://pusat.jakarta.go.id/?mod=main&sub=info&action=news_cat&id=1', 'http://pusat.jakarta.go.id/?mod=main&sub=info&action=news_cat&id=2', 'http://pusat.jakarta.go.id/?mod=main&sub=info&action=news_cat&id=3', 'http://pusat.jakarta.go.id/?mod=main&sub=info&action=news_cat&id=4' ]

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//h5[@class="media-heading"]/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="page-head"]/h3/text()'))
        text = textify(hdoc.select('//div[contains(@class, "page-content")]//text()'))
        date = textify(hdoc.select('//div[@class="entry-meta"]/span/text()')).split(',')[-1].strip()
        month = date.split(' ')[1]
        s = {'January':'Januari','February':'Februari','March':'Maret','April':'April','May':'Mei','June':'Juni','July':'Juli','August':'A    gustus','September':'September','October':'Oktober','November':'Nopember','December':'Desember'}
        s1 = {'January':'Januari','February':'Februari','March':'Maret','April':'April','May':'Mei','June':'Juni','July':'Juli','August':'Agustus','September':'September','October':'Oktober','November':'Nopember','December':'Desember'}
        dt_added = ''
        for key,value in s.iteritems():
            if key in month:
               eng_month = key
               date = date.replace(month,eng_month)
               dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        for key,value in s1.iteritems():
            if value in month:
               eng_month = key
               date = date.replace(month,eng_month)
               dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))

        print '/n'
        print response.url
        print 'title' ,xcode(title)
        print 'text' ,xcode(text)
        print 'dt_added' ,xcode(dt_added)
