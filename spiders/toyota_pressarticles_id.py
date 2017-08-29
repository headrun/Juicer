from juicer.utils import *
from dateutil import parser

class ToyotaPressArticles(JuicerSpider):
    name = 'toyota_pressarticles'
    start_urls = ['http://www.toyota.astra.co.id/livebeta/index.php?page.offset=0&page.total=233&page.size=6&act=pressroom&p_id=siaran-pers&sub=list']

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
            check_date = self._latest_dt + datetime.timedelta(hours=7)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        is_next = True
        links = hdoc.select('//ul/li')

        for link in links:
            date = textify(link.select('.//span[@class="date"]/text()'))
            date_dict = {'January':'Januari','February':'Februari','March':'Maret','April':'April','May':'Mei','June':'Juni','July':'Juli','August':'Agustus','September':'September','October':'Oktober','November':'Nopember','December':'Desember'}
            month = date.split(' ')[1]
            for key,value in date_dict.iteritems():
                if month == value: month= key
            date = date.split(' ')[0] + ' '+ month +  ' ' + date.split(' ')[-1]
            dt_added1 = parse_date(xcode(date))
            if dt_added1 < self.cutoff_dt:
                is_next = False
                continue
            news_link = textify(link.select('./a[@title]/@href'))
            if 'http' not in news_link: news_link ='http://www.toyota.astra.co.id'+news_link
            yield Request(news_link,self.parse_details,response)

        next_page = textify(hdoc.select('//a[contains(text(),"next")]/@rel'))
        if next_page and is_next:
            yield Request(next_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@name="Fact Sheet"]//h1/text()'))
        dt_added = textify(hdoc.select('//div[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=9))
        text = textify(hdoc.select('//div[@name="Fact Sheet"]//p//text()'))

        item = Item(response)
        item.set('url', response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        yield item.process()


