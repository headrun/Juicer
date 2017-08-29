from juicer.utils import *
from dateutil import parser

class ThemonthlyAU(JuicerSpider):
    name = 'themonthly'
    start_urls = ['https://www.themonthly.com.au/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="links secondary-links inline"]/li/a/@href').extract()
        for category in categories:
            if 'http' not in category: category =  'https://www.themonthly.com.au' + category
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="view-content"]//span/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'https://www.themonthly.com.au' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next"]//a[@title="Go to next page"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'https://www.themonthly.com.au' + nxt_pg
        yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title"]/text()'))
        text = textify(hdoc.select('//div[@class="content-inner"]/p//text()')) or textify(hdoc.select('//div[@class="teaser-wrapper"]/p//text()'))
        add_txt = textify(hdoc.select('//h3[@class="subtitle"]//text()'))
        text = add_txt + ' ' + text
        date=textify(hdoc.select('//div[contains(@class, "submitted-date")]//text()').extract()) or textify(hdoc.select('//span[@class="issue-title"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))

        author = textify(hdoc.select('//div[contains(@class, "donothyphenate")]//span[@class="author-name"]/a/text()')) or textify(hdoc.select('//div[@class="submitted"]//a/text()'))
        author_url = textify(hdoc.select('//div[contains(@class, "donothyphenate")]//span[@class="author-name"]/a/@href')) or textify(hdoc.select('//div[@class="submitted"]//a/@href'))
        if 'http' not in author_url: author_url = 'https://www.themonthly.com.au' + author_url


        item = Item(response)
        item.set('url', response.url)
        item.set('title' ,xcode(title))
        item.set('text' ,xcode(text))
        item.set('dt_added' ,dt_added)
        item.set('author' ,{'name':xcode(author)}) 
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','australia_country_manual'])
        yield item.process()
