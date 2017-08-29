from juicer.utils import*
from dateutil import parser

class Hindustantimes_IN(JuicerSpider):
    name = 'hindustantimes'
    start_urls = ['http://www.hindustantimes.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="col-xs-6 col-sm-2 footer-list"]//li[not(contains(@class, "column-head"))]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.hindustantimes.com' + cat
            yield Request(cat,self.parse_links,response)
        
    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="media-body"]/div[@class="media-heading headingfour"]/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        ext_links = hdoc.select('//div[@class="row pb-30"]//div[@class="headingfour"]/a/@href | //div[@class="media-heading headingfive"]/a/@href').extract() or hdoc.select('//ul[@class="clearfix"]//a/@href').extract()

        for lin in ext_links:
            yield Request(lin,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="story-highlight"]//h1[@itemprop="headline"]//text()')) or textify(hdoc.select('//h1[contains(@class, "head")]//text()')) or textify(hdoc.select('//div[@class="video-heading"]//h1//text()')) or textify(hdoc.select('//h1//text()'))
        add_txt = textify(hdoc.select('//div[@class="story-highlight"]//h2//text()')) or textify(hdoc.select('//h2[@class="dek"]//text()'))
        txt = textify(hdoc.select('//div[@itemprop="articlebody"]//p//text()')) or textify(hdoc.select('//div[@class="copy"]//p//text()')) or textify(hdoc.select('//div[@class="video-summary mt-20 mb-20"]//text()')) or textify(hdoc.select('//div[@class="copy-container"]//text()')) or textify(hdoc.select('//div[@itemprop="articlebody"]//text()')) or textify(hdoc.select('//div[contains(@class, "container")]//text()'))
        date = textify(hdoc.select('//meta[@itemprop="datePublished"]/@content')) or textify(hdoc.select('//div[@class="updated-date"]//text()')) or textify(hdoc.select('//h3[@class="byline dateline"]//text()'))
        if not date:
            dt = textify(hdoc.select('//h2[@class="byline"]//text()')) or textify(hdoc.select('//span[@class="date"]//text()'))
            date = ''.join(re.findall('\| (.*?)$', dt))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//div[@itemprop="author"]//span[@itemprop="name"]//text()')) or textify(hdoc.select('//h3[@class="byline"]//text()'))
        add_text = textify(hdoc.select('//div[@class="img-captionh2"]//text()'))
        add_txt = add_txt + ' ' + add_text
        if not author:
            auth = textify(hdoc.select('//h2[@class="byline"]//text()')) or textify(hdoc.select('//span[@class="date"]//text()'))
            author = auth.partition('|')[0]
        author = author.replace('By','').replace('by','')
        junk_txt = textify(hdoc.select('//div[@class="video-summary-head"]//text()')) or textify(hdoc.select('//div[@itemprop="articlebody"]//strong//text()'))

        txt = txt.replace(junk_txt,'')
        text = add_txt + ' ' + txt

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()


