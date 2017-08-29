from juicer.utils import*
from dateutil import parser

class Wenweipo(JuicerSpider):
    name = 'wenweipo'
    start_urls = ['http://news.wenweipo.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//td[@valign="top"]//a[contains(@href,"list.php")]/@href').extract()
        for category in categories:
            if 'http' not in category:
                category = 'http://news.wenweipo.com' + category
                yield Request(category,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@id="content"]//a[contains(@class,"sub_fg16")]')
        for node in nodes[:2]:
            link = textify(node.select('./@href'))
            full_date = textify(hdoc.select('//td[@class="sub_fk14"]/text()'))
            date = '/'.join(re.findall('\d+',full_date))
            full_time = textify(node.select('./../span/text()'))
            time = ':'.join(re.findall('\ \d+:.*',full_time)).replace(']','')
            date = date + ' ' + time
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = 'http://news.wenweipo.com/2016/09/21/IN1609210046.htm'
            yield Request(link,self.parse_final,response)

        next_page = textify(hdoc.select('//iframe[@name="datamain"]/@src'))
        if next_page:
            yield Request(next_page,self.parse_details)

        all_dates_from_calender = hdoc.select('//table[@id="calendar-news-table"]/tr/td/a[contains(@href,"http://news.wenweipo.com")]/@href').extract()
        for date in all_dates_from_calender:
            yield Request(date,self.parse_details)

        '''
        next_page = textify(hdoc.select('//iframe[@name="datamain"]/@src'))
        if next_page:
            date =  int(re.findall('&day=(\d+)',next_page)[0])
            for day in range(1,date+1):
                day = str(day)
                year = re.findall('&year=(\d+)',next_page)[0]
                month = re.findall('&month=(\d+)',next_page)[0]
                if len(day)==1:
                    day='0'+day
                else:
                    day=day
                link = 'http://news.wenweipo.com/list_srh.php?cat=000IN&'+next_page.split('&')[-1]+'&date='+str(year)+str(month)+str(day)
                yield Request(link,self.parse_details,response)
        '''


    def parse_final(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//h1[@class="title"]/text()'))
        author = ''.join(hdoc.select('//p[@class="fromInfo"]/text()').extract()).encode('utf-8').split('\xaf\xef\xbc\x9a')[-1]
        text = textify(hdoc.select('//div[@id="main-content"]/p//text()')).encode('utf-8').replace(author,'')
        date = textify(hdoc.select('//span[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))

        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author.name',xcode(author)

