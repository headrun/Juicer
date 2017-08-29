from juicer.utils import *

from datetime import date

class Spider(JuicerSpider):
    name = 'feedcamp'
    allowed_domains = ['feedcamp.com']
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    start_urls = ["http://www.feedcamp.com/top-feeds/?d=" + today]
    #start_urls = ['http://www.feedcamp.com/top-feeds/?d=2011-10-6']

    def parse(self, response):
        hdoc = HTML(response)
        keywords = hdoc.select('//td[@class="p_text_sm"]//a[@rel="nofollow"]/text()')
        keywords = [textify(xcode(k)) for k in keywords]
        urls = ['http://www.rssmicro.com/temp/feedsearch.aspx?sd=undefined&sit=2&or=r&st=%s&rst=0&cnt=0&ref=http://www.rssmicro.com/?q=%s&f=3&sd=0&p=2&sp=1' %(key, key) for key in keywords]
        for url in urls:
            item = Item(response)
            item.spider = 'rssmicro'
            yield item.set_many({'sk': md5(url), 'got_page': False, 'url': url}).process()
        omgili_urls = ['http://omgili.com/api.search?obd=0&q=%s&p=1' %key for key in keywords]
        for url in omgili_urls:
            get_page('omgili', url)

