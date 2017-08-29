from juicer.utils import *
from dateutil import parser

class QingdaonewsForum(JuicerSpider):
    name = 'qingdaonews_forum_china'
    start_urls = ['http://club.qingdaonews.com/']
    def parse(self,response):
        hdoc = HTML(response)
        #import pdb;pdb.set_trace()
        nodes = hdoc.select('//div[@class="nav_list"]//div[@id="rA1"]//ul//li')
        for node in nodes[:1]:
            node = textify(hdoc.select('.//a//@href'))
            node = 'http://club.qingdaonews.com/club_entry_129_3_0_1_0.htm'
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        #import pdb;pdb.set_trace()
        urls = hdoc.select('//table[@class="list_data mb15"]//div[@class="qtit"]//a[contains(@href , "/showAnnounce")]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="tit"]//h2//text()'))
        text = textify(hdoc.select('//div[@class="text"]//text()'))
        dt_added = textify(hdoc.select('//div[@class="article_foot"]/span/text()')[0])
        print "title:::",xcode(title)
        print "text::::",xcode(text)
        print "date::::",xcode(dt_added)

