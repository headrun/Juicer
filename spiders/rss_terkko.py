import httplib

from juicer.utils import *

class TerkkoSpider(JuicerSpider):
    name = 'rss_terkko'
    start_urls = 'http://www.terkko.helsinki.fi/feednavigator/?c=Blogit'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//table[@class="fn2"]//td//a[@title]/@href', response)
        for url in urls:
            url = xcode(textify(url))
            yield Request(url,self.parse,response)

        next_url = hdoc.select_urls('//a[contains(text(), "next")]/@href', response)
        yield Request(next_url,self.parse,response)

        terminal_urls = hdoc.select_urls('//table[@class="fn"]//td//a[@id]/@href', response)
        for url in terminal_urls:
            if '.blogspot.' in url:
                url = xcode(textify(url))
                url = url.split('/')[2]
                url = 'http://' + url + '/feeds/posts/default'
            elif '/blogs.' or '/blogit.' in url:
                url = xcode(textify(url))
                url = url + 'feed/'
            else:
                url = xcode(textify(url))
                url = url + '/feed/'
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            #print doc

            try:
                TerkkoSpider.db.insert(TerkkoSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                #print 'BadStatusLine error'
                continue
        got_page(self.name, response)
