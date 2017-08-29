from juicer.utils import *
from dateutil import parser

class MeizuForum(JuicerSpider):
    name = 'meizu_forum_china'
    start_urls = ['http://bbs.meizu.cn/forum.php?mod=forum']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="content"]//ul//li')
        for node in nodes:
            node = textify(node.select('.//a//@href'))
            print node
            #yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('')
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
