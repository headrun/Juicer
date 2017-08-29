from juicer.utils import *
from dateutil import parser
from scrapy.http import FormRequest

class ToyotaIndonesia(JuicerSpider):
    name = 'toyota_indonesia'
    start_urls = ['http://www.toyota.astra.co.id/connect/news/berita/','http://www.toyota.astra.co.id/connect/news/teknologi/','http://www.toyota.astra.co.id/connect/news/travelling/','http://www.toyota.astra.co.id/connect/news/lifestyle/','http://www.toyota.astra.co.id/connect/news/kuliner/','http://www.toyota.astra.co.id/connect/news/fotografi/','http://www.toyota.astra.co.id/connect/news/komunitas/','http://www.toyota.astra.co.id/connect/news/tips/','http://www.toyota.astra.co.id/connect/toyota-event/event/','http://www.toyota.astra.co.id/connect/toyota-event/competition/']

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

        _id = textify(hdoc.select('//div//img/@data-plugin')).split('"item":')[-1].strip('}').strip('"')
        headers = {'type':'list','status':'frontend','pid':_id,'to':'10'}
        url = 'http://www.toyota.astra.co.id/connect/content/'
        yield FormRequest(url,self.parse_next,formdata=headers,meta={'id1':_id})

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//li/a[@title=""]')
        for link in links:
            article_link = textify(link.select('./@href'))
            date = textify(link.select('.//span[@class="date"]/text()'))
            date = parse_date(xcode(date))
            if date < self.cutoff_dt:
                is_next = False
                continue
            dt_added1 = get_timestamp((date) - datetime.timedelta(hours=9))
            if 'http' not in article_link: article_link = 'http://www.toyota.astra.co.id' + article_link
            yield Request(article_link,self.parse_details,response,meta={'dt_added':dt_added1})

        next_page = textify(hdoc.select('//div/a[@id="btn_explore"]/@href'))
        if next_page and is_next:
            next_link = 'http://www.toyota.astra.co.id/connect/content/'
            header1 = {'type':'list','status':'frontend','pid':response.meta['id1'],'to':next_page}
            yield FormRequest(next_link,self.parse_next,formdata=header1,meta={'id1':response.meta['id1']})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="description"]/h2/text()')) or textify(hdoc.select('//div[contains(@class, "content_fact_sheet_detail")]/h1/text()'))
        text = textify(hdoc.select('//div[contains(@class,"text_box")]//div[not(contains(@class,"author"))]//text() | //div[contains(@class,"text_box")]//b//text() | //div[contains(@class,"text_box")]//p//text() | //div[@class="page_area"]//p//text()'))
        tags = textify(hdoc.select('//div[@class="tags"]//text()'))
        if tags != '':text = textify(text.split('TAGS:')[0])
        dt_added = response.meta['dt_added']
'''
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        #yield item.process()'''
