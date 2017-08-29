from juicer.utils import *
from scrapy.http import FormRequest

class CarMy(JuicerSpider):
    name = 'carmy'
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
        #if 'prnewswire' in response.url:
            #pr_link = 'http://tools.prnewswire.com/en-us/live/4693/list/landing?start=1&filter=4693'
            #yield Request(pr_link,self.parse_extraurls,response)

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

    '''def parse_extraurls(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//li[@class]')
        for url in urls[:2]:
            dt = textify(url.select('.//span[contains(@class,"time")]/text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)))
            news_url = textify(url.select('.//a/@href')).split('?rkey=')[-1].split('&')[0]
            news_url = 'http://tools.prnewswire.com/en-us/live/4693/release/%s'%news_url
            yield Request(news_url,self.parse_details,response)

        nxt_page = response.url.split('?start=')[-1].split('&')[0]
        if nxt_page:
            nxt_page =  1 + int(nxt_page)
            nxt_page = 'http://tools.prnewswire.com/en-us/live/4693/list/landing?start=%s&filter=4693' %nxt_page
            yield Request(nxt_page,self.parse_extraurls,response)'''

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name"]/text()')) or textify(hdoc.select('//h1/text()'))
        date = hdoc.select('//p[@class="dateTime"]/text()').extract() or hdoc.select('//span[@class="xn-chron"]/text()').extract()
        if len(date) > 1:date = textify(date[0])
        else:date = textify(date)
        dt_added = get_timestamp(parse_date(date)-datetime.timedelta(hours=8))
        text = textify(hdoc.select('//span[@itemprop="articleBody"]/p//text() | //span[@itemprop="articleBody"]/div//text()')) or textify(hdoc.select('//p//text()'))

        print '\n'
        print 'url',response.url
        print 'title',xcode(title)
        print 'dt_added',dt_added
        print 'text',xcode(text)
