from juicer.utils import *
from scrapy.http import FormRequest

class CarMy(JuicerSpider):
    name = 'carmalaysia'
    start_urls = ['http://carmalaysia.my']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//li/a[not(contains(@data-toggle,"dropdown"))]/@href').extract()
        for link in links:
            if 'Home.aspx' in link:continue
            if 'http' not in link: link = 'http://carmalaysia.my' + link
            yield Request(link,self.parse_urls,response)

    def parse_urls(self,response):
        hdoc = HTML(response)

        news_links = hdoc.select('//div[contains(@class,"listMore")]/a/@href').extract()
        for news_link in news_links:
            yield Request(news_link,self.parse_details,response)

        next_page = textify(hdoc.select('//li[@class="Next"]/a/@href'))
        if next_page:
            next_url = response.url
            next_page = textify(re.findall('\d+',next_page)).strip(' ')
            value = textify(hdoc.select('//input[@id="__VIEWSTATE"]/@value')).strip(' ')
            data = {'manScript_HiddenField':'',
                    '__EVENTTARGET':'p$lt$Main$Content$p$lt$Content$APUBArticleListing$uniPager',
                    '__EVENTARGUMENT':next_page,
                    'lng':'en-US',
                    'search':'',
                    '__VIEWSTATE':value}
            yield FormRequest(next_url,self.parse_urls,formdata=data)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name"]/text()'))
        date = textify(hdoc.select('//p[@class="dateTime"]/text()'))
        dt_added = get_timestamp(parse_date(date)-datetime.timedelta(hours=8))
        text = textify(hdoc.select('//span[@itemprop="articleBody"]/p//text() | //span[@itemprop="articleBody"]/div//text()'))

        if dt_added > get_current_timestamp()-86400*30:
            print '\n'
            print 'url',response.url
            print 'title',xcode(title)
            print 'date',dt_added
            print 'text',xcode(text)
