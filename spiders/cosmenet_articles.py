from juicer.utils import *
from dateutil import parser

class CosemenetArticles(JuicerSpider):
    name = 'cosmenet_articles'
    start_urls = ['http://www.cosmenet.in.th/update/']

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
        nodes = hdoc.select('//div[@class="item-post "]')

        for node in nodes:
            links = textify(node.select('.//div[@class="field-content"]/a/@href'))
            post_date = textify(node.select('.//span[@class="post-date"]/text()'))
            post_dtadded = parse_date(post_date)
            if post_dtadded < self.cutoff_dt:
                is_next = False
                continue
            if 'http' not in links: links = 'http://www.cosmenet.in.th' +xcode(links)
            yield Request(links,self.parse_details,response)

        next_pg = textify(hdoc.select('//a[@id="next"]/@href'))
        if next_pg and 'load_page' in response.url and is_next:
            next_pg = int(textify(response.url.split('?p=')[-1])) + 1
            next_pg = 'http://www.cosmenet.in.th/update/load_page.php?p=' + str(next_pg)
        elif next_pg and is_next:next_pg = 'http://www.cosmenet.in.th/update/' + next_pg
        yield Request(next_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="update-detail"]//h1/text()'))
        date = textify(hdoc.select('//span[@class="post-date"]/text()'))
        dt_added  = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
        views = textify(hdoc.select('//div[@class="pageview"]/span/text()'))
        text = textify(hdoc.select('//div[@class="detail_text"]//text()'))

        item = Item(response)
        item.set('url', response.url)
        item.set('title',xcode(title))
        item.set('dt_added',xcode(dt_added))
        item.set('views',views)
        item.set('text',xcode(text))
        yield item.process()
