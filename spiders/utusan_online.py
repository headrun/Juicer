from juicer.utils import *
from dateutil import parser

class Utusan(JuicerSpider):
    name = "utusan"
    start_urls = ['http://www.utusan.com.my/']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="sitemap_nav_block"]//a/@href').extract()
        for url in urls:
            if 'http' not in url: url = 'http://www.utusan.com.my' + url
            yield Request(url, self.parse_links, response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="item_content"]/following-sibling::a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.utusan.com.my' + link
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[contains(@class, "articleTitle content")]//text()'))
        date=textify(hdoc.select('//time[@itemprop="datePublished"]/text()'))
        if 'Januari' in date:
            date = date.replace('Januari','Jan')
        elif 'Februari' in date:
            date = date.replace('Februari','Feb')
        elif 'Mac' in date:
            date = date.replace('Mac','March')
        elif 'Mei' in date:
            date = date.replace('Mei',"May")
        elif 'Julai' in date:
            date = date.replace('Julai','July')
        elif 'Ogos' in date:
            date = date.replace('Ogos','Aug')
        elif 'Oktober' in date:
            date = date.replace('Oktober','Oct')
        elif 'Disember' in date:
            date = date.replace('Disember','Dec')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[contains(@class, "article_body content__article-body")]//text()'))
        add_txt = textify(hdoc.select('//div[@class="content__standfirst"]//p//text()')) 
        text = add_txt + ' ' + text
        author = textify(hdoc.select('//meta[@name="author"]/@content')) 
        

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags', ['news_sourcetype_manual', 'malaysia_country_manual'])
        yield item.process()


