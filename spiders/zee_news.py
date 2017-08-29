from juicer.utils import*
from dateutil import parser

class ZeeNews(JuicerSpider):
    name = "zee_news"
    start_urls = ['http://zeenews.india.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@data-event-sub-cat="Navigation"]/li[contains(@id,"nav")]//a/@href').extract()
        for category in categories:
            if 'http' not in category: category = 'http://zeenews.india.com' + category
            if 'http://zeenews.india.com' in category:yield Request(category, self.parse_next, response)

    def parse_next(self, response):
        hdoc = HTML(response)
        news_links = hdoc.select('//p[contains(@class,"story-head-pa")]/a/@href\
                            | //span[contains(@class,"lead-health-ab")]/a/@href').extract()

        for news_link in news_links:
            if 'http' not in news_link: news_link = 'http://zeenews.india.com' + news_link
            yield Request(news_link, self.parse_details, response)

        nxt_pg = textify(hdoc.select('//li[@class="next last"]/a/@href'))
        if nxt_pg:
            if 'http' not in nxt_pg: nxt_pg = 'http://zeenews.india.com' + nxt_pg
            yield Request(nxt_pg, self.parse_next, response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="full-story-head"]//h1//text() | //h1/text()'))
        text = textify(hdoc.select('//div[@class="field-item even"]//p//text()'))
        add_txt = textify(hdoc.select('//p[@class="head-para"]//text()'))
        text = add_txt + ' ' + text
        dt = textify(hdoc.select('//meta[@property="article:published_time"]/@content'))
        #date = ''.join(re.findall('(.*)\T',dt))
        dt=dt.replace('T',',')
        date = dt.partition('+')[0]
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
        auth = textify(hdoc.select('//div[@class="article-date-block"]//text()'))
        if 'By' in auth:
            author = auth.partition('|')[0]
            author = author.replace('By','')
        
            item = Item(response)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('author',{'name':xcode(author)})
            item.set('xtags',['news_sourcetype_manual','india_country_manual'])
            yield item.process()

        else:
            item = Item(response)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('xtags',['news_sourcetype_manual','india_country_manual'])
            yield item.process()
