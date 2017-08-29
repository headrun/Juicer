from juicer.utils import*
from dateutil import parser

class Sinarharian_MY(JuicerSpider):
    name = 'sinarharian_my'
    start_urls = ['http://www.sinarharian.com.my/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [301,302]


    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="col-footer"]//ul//li/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.sinarharian.com.my' + cat
            if '/play.google.com/' in cat or '/www.youtube.com/' in cat or '/www.instagram.com/' in cat or '/twitter.com/' in cat or '/www.facebook.com/' in cat:
                continue
            yield Request(cat,self.parse_links,meta = {'dont_redirect':True})

    def parse_links(self,response):
        hdoc = HTML(response)
        if '/Edisi' or 'edisi' in response.url:
            links = hdoc.select('//li[5]//a/@href').extract()
            for link in links:
                if 'http' not in link: link  = 'http://www.sinarharian.com.my' + link
                yield Request(link,self.parse_oth_links,response)
        links = hdoc.select('.//div[@class="title-teaser"]/a/@href').extract()
        for link in links:
            if 'http' not in link: link  = 'http://www.sinarharian.com.my' + link
            if '/video/' in link:
                continue
            yield Request(link,self.parse_details,response)
    def parse_oth_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('.//div[@class="title-teaser"]/a/@href').extract()
        for link in links:
            if 'http' not in link: link  = 'http://www.sinarharian.com.my' + link
            if '/video/' in link:
                continue
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@itemprop="name"]//text()'))
        ext_txt = textify(hdoc.select('//div[@class="img-caption"]//text()'))
        text = textify(hdoc.select('//div[@id="articleBody"]//p//text()'))
        text = ext_txt + ' ' + text
        date = textify(hdoc.select('//div[@itemprop="datePublished"]/@content'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        auth = textify(hdoc.select('//div[@class="author"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(auth)})
        item.set('xtags',['news_sourcetype_manual','malaysia_country_manual'])
        yield item.process()

