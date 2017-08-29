from juicer.utils import *
from dateutil import parser

class ConsumercomplaintsIndia(JuicerSpider):
    name = 'consumer_complaintsindia'
    start_urls = ['http://www.consumercomplaints.in/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//td[@class="complaint"]/ancestor::div[@id]')
        for node in nodes:
            date = textify(node.select('.//a[contains(@href,"profile")]/parent::td/text()')).split('on')[-1]
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*1:
                is_next = False
                continue
            link = textify(node.select('.//td[@class="complaint"]//h4/a/@href'))
            if 'http' not in link: link = 'http://www.consumercomplaints.in' + link
            yield Request(link,self.details,response)

        next_page = textify(hdoc.select('//div[@class="pagelinks"]//a[contains(text(),"Next")]/@href'))
        if next_page and is_next:
            next_page = 'http://www.consumercomplaints.in' + next_page
            yield Request(next_page,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td[@class="complaint"]/h1/text()'))
        author = textify(hdoc.select('//table[@typeof="v:Review-aggregate"]//td[@class="small"]/a[contains(@href,"profile")]/text()'))
        dt = textify(hdoc.select('//table[@typeof="v:Review-aggregate"]//td[@class="small"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=5,minutes=30))
        text = textify(hdoc.select('//td[@class="compl-text"]/div[not(contains(@class,"resolved-text"))]//text()'))

        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'author',xcode(author)
        print 'dt_added',dt_added
        print 'text',xcode(text)
