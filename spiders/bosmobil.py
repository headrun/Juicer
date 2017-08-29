from juicer.utils import *
from datetime import date

class Bosmobil(JuicerSpider):
    name = "bosmobil"
    allowed_domains = ['bosmobil.com']
    start_urls = ['http://www.bosmobil.com/category/audio/','http://www.bosmobil.com/category/berita/','http://www.bosmobil.com/category/berita/berita-global/','http://www.bosmobil.com/category/berita/berita-nasional/','http://www.bosmobil.com/category/review/','http://www.bosmobil.com/category/modifikasi/','http://www.bosmobil.com/category/komunitas/','http://www.bosmobil.com/category/produk/']

    def parse(self, response):
        hdoc =  HTML(response)
        is_next = True
        if self.latest_dt: self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        check_date = self._latest_dt + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_date - oneweek_diff 
        nodes = hdoc.select('//div[contains(@class,"post-wrapper")]')
        for node in nodes:
            post_date = parse_date(textify(node.select('.//span[@itemprop="datePublished"]/text()')))
            if post_date < self.cutoff_dt:
                is_next = False
                continue
            url = textify(node.select('.//h2/a/@href'))
            yield Request(url,self.parse_mobil,response)

        next_page_link = textify(hdoc.select('//link[@rel="Next"]/@href'))
        if next_page_link and is_next:
            yield Request(next_page_link,self.parse,response)

     def parse_mobil(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="content"]//h1/text()'))
        author = textify(hdoc.select('//div[@class="meta-item author"]//span[@itemprop="name"]/text()'))
        date = textify(hdoc.select('//span[@class="updated"]/text()'))
        date = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@itemprop="text"]//p//text()'))
        tag = textify(hdoc.select('//li/a[@rel="tag"]/text()'))
        views = textify(hdoc.select('//div[@class="meta-item views"]/text()'))
        num = {'views': int(views.replace('Views', ''))}

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'date',xcode(date)
        print 'tag',xcode(tag)
        print 'views',xcode(views)


