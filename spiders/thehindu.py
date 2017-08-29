from juicer.utils import*
from dateutil import parser

class TheHindu_IN(JuicerSpider):
    name = 'thehindu'
    start_urls = ['http://www.thehindu.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="sub-menu"]//li/a/@href | //li/a[contains(text(), " Children ")]/@href | //li/a[contains(text(), "Real Estate")]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="search-scrollar"]//following-sibling::div[@class="row"]//h3/a/@href').extract() or hdoc.select('//div[@class="Other-StoryCard"]/h3/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = ''.join(set(hdoc.select('//div[@class="main"]//li[@class="next page-item"]/a[@class="page-link"]/@href').extract()))
        yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title"]//text()')) or textify(hdoc.select('//h1[@class="special-article-heading"]//text()')) or textify(hdoc.select('//h1[contains(@class, "special-heading")]//text()')) or textify(hdoc.select('//div[contains(@class, "article")]//h1//text()'))
        add_txt = textify(hdoc.select('//h2[@class="intro"]//text()'))
        text = textify(hdoc.select('//div[contains(@id, "content-body-")]//p//text()'))
        text = add_txt + ' ' + text
        date=textify(hdoc.select('//div[@class="ut-container"]//span[@class="blue-color ksl-time-stamp"]//none'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//a[@class="auth-nm lnk"]//text()')) or textify(hdoc.select('//a[@class="auth-nm no-lnk"]//text()'))
        author_url = textify(hdoc.select('//a[@class="auth-nm lnk"]//@href'))


        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
