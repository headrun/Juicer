from juicer.utils import *
from dateutil import parser

class PragativadiIN(JuicerSpider):
    name = 'pragativadi'
    start_urls = ['http://pragativadi.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//a[@tabindex="0"]/@href | //a[contains(@class, "dashicons-")]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)



    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div//a[@rel="bookmark"]/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//link[@rel="next"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="post-title entry-title left"]//text()'))
        date=textify(hdoc.select('//time[@itemprop="datePublished"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//span[@class="author-name vcard fn author"]/a[@rel="author"]//text()'))
        author_url = textify(hdoc.select('//span[@class="author-name vcard fn author"]/a[@rel="author"]//@href'))
        text = textify(hdoc.select('//div[@id="content-main"]//p//text()')) or textify(hdoc.select('//div[@id="content-main"]//div//text()'))
        add_junk = textify(hdoc.select('//div[@id="article-ad"]//text()'))
        junk = textify(hdoc.select('//div[@class="post-tags"]//text()')) 
        text = text.replace(junk,'').replace(add_junk,'')
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)}) 
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield  item.process()


