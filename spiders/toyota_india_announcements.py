from juicer.utils import *

class ToyotaIndiaAnnouncement(JuicerSpider):
    name = "toyota_india_announcement"
    start_urls = ['http://www.toyotabharat.com/inen/announcement.aspx']
    def parse(self,response):
        hdoc = HTML(response)
        text = textify(hdoc.select('//tr//td//text()'))
        print xcode(text)
