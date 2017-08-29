from juicer.utils import *
from dateutil import parser

class PcdvdTaiwan(JuicerSpider):
    name = 'pcdvd_tw'
    start_urls = ['http://pcdvd.com.tw/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//td[@class="alt1Active"]/div/a[contains(@href,"forum")]/@href').extract()
        for link in links[:2]:
            if 'http' not in link:link = 'http://pcdvd.com.tw/' + link
            yield Request(link,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        thread_links = hdoc.select('//div[@style="text-align:right; white-space:nowrap"]/parent::td')
        for thread_link in thread_links[:2]:
            date = textify(thread_link.select('.//span[@class="time"]/parent::div/text() | .//span[@class="time"]/text()'))
            date = ' '.join(textify(date).split(' ')[:3])
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            threadlink = textify(thread_link.select('./following-sibling::td/a[contains(@href,"goto=lastpost")]/@href')).split('&')[-2:]
            import pdb;pdb.set_trace()
            if 'http' not in threadlink: threadlink = 'http://pcdvd.com.tw/showthread.php?' + '&'.join(threadlink)
            #threadlink = 'http://pcdvd.com.tw/showthread.php?p=%s#post%s'%(threadlink,threadlink)
            yield Request(threadlink,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
