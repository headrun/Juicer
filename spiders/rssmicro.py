from juicer.utils import *

class RssMicroSpider(JuicerSpider):
    name = 'rssmicro'
    allowed_domains = ['rssmicro.com']
    
    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        page_number = response.url.split('sp=')
        next_link = hdoc.select('//a[contains(text(),"Next")]')
        if next_link and page_number:
            next_page_url = page_number[0] + "sp=%d" % (int(page_number[-1]) + 1)
            print "Next_page_url: ==============>", next_page_url
            yield Item(response).set_many({'got_page': False, 'url': next_page_url}).process()
        feed = hdoc.select_urls(['//div[@class="p_text_sm_link"]/text()'], response)
        doc = {'url':feed, 'url_hash':md5(feed), 'last_run':0, 'next_run':0}
        try:
            RssMicroSpider.db.insert(self.db_name, "rss", doc=doc)
            yield item.set_many({ 'got_page': True, 'rss_url': feed }).process()
        except httplib.BadStatusLine:
            # ignoring error. needs to be debugged in cloudlibs dbservice
            print 'BadStatusLine error'


