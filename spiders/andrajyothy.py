from juicer.utils import*
from dateutil import parser

class AndhrajyothyNews(JuicerSpider):
    name = "andhrajyothy_news"
    start_urls = ['http://www.andhrajyothy.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="navbar-default"]//li/a[not(contains(@href,"http"))]/@href').extract()
        for category in categories:
            if 'http' not in category:
                category = 'http://www.andhrajyothy.com/' + category
                yield Request(category, self.parse_links, response)


    def parse_links(self,response):
        hdoc = HTML(response)
        if response.url == 'http://www.andhrajyothy.com/':
            news_urls = hdoc.select('//ul[@id="menu"]//li/a/@href').extract()
            extra_urls = hdoc.select('//div[contains(@class, "main-news")]//div/a/@href').extract()
        else:
            news_urls = []
            extra_urls = hdoc.select('//div[contains(@class, "main-news")]//div/a/@href').extract() or hdoc.select('//div[@class="padd-left padd-left-resp-right margin-top"]//div/a/@href').extract() or hdoc.select('//table[contains(@id, "ContentPlaceHolder1_dlst")]//span/a/@href').extract() or hdoc.select('//article[@class="telugu-font"]//a/@href').extract()
        news_urls.extend(extra_urls)
        for url in news_urls:
            if 'openheartarticle' in url or 'PDF' in url or 'edu.andhraj' in url:
                continue
            if 'Article?SID' in url or "../Artical.aspx?" in url:
                yield Request(url, self.parse_details, response)
            else:
                yield Request(url, self.parse_links, response)
        more_urls = hdoc.select('//div[@class="more-block"]//ul//li//a/@href').extract()
        for more_url in more_urls:
            more_url = 'http://www.andhrajyothy.com/artical?SID=316750'
            yield Request(more_url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = xcode(textify(hdoc.select('//div[@class="article telugu-font"]/h3/span[@id="ContentPlaceHolder1_lblStoryHeadLine"]/text() |//div[@class="module-hd-telugu telugu-font"]/span/text()').extract())) or xcode(textify(hdoc.select('//p[@class="telugu-font"]/span[@id="ContentPlaceHolder1_lblNavTitle"]/text()')))
        text = xcode(textify(hdoc.select('//div[contains(@class, "detailsAbnBody")]//text()'))) or xcode(textify(hdoc.select('//div[@class="detailsAbnBody imgsdiv"]//div//text()'))) or xcode(textify(hdoc.select('//div[@class="detailsAbnBody imgsdiv"]/span/text()'))) or xcode(textify(hdoc.select('//div[@id="pastingspan1"]//text()')))
        date = xcode(textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblUpdatedDate"]/text()').extract()))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
            
        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)

'''         item = Item(response)
            item.set('url', response.url)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', dt_added)'''
            #yield item.process()
