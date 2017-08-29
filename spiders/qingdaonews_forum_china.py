from juicer.utils import *
from dateutil import parser

class QingdaonewsForum(JuicerSpider):
    name = 'qingdaonews_forum_china'
    start_urls = ['http://club.qingdaonews.com/']
    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="nav_list"]//div[@id="rA1"]//ul//li')
        for node in nodes:
            node = textify(node.select('.//a//@href'))
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//table[@class="list_data mb15"]//div[@class="qtit"]//a//@href')
        for url in urls:
            url = textify(url)
            forum_title = textify(hdoc.select('//div[@id="container"]//div[@class="breadcrumb"]//a[contains(@href ,"club_entry_")]/text()'))
            forum_title = forum_title.split(' ')
            forum_title = forum_title[0]
            yield Request(url,self.parse_details,response,meta = {'forum_title':forum_title})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="tit"]//h2//text()'))
        text = textify(hdoc.select('//div[@class="text"]//text()'))
        dt_added = textify(hdoc.select('//div[@class="article_foot"]/span/text()'))
        print "title:::",xcode(title)
        print "text::::",xcode(text)
        print "date::::",xcode(dt_added)
        print "thread_url::",response.url

