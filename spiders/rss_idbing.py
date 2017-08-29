import httplib

from juicer.utils import *

class IdBing7Spider(JuicerSpider):
    name = 'rss_idbing7'
    start_urls = ['http://www.bing.com/search?q=feed%3A+inbody%3Atravel+insurance+location%3Aid&go=&qs=n&form=QBRE&filt=all&pq=feed%253A%2520inbody%253Atravel%2520insurance%2520location%253Aid&sc=0-0&sp=-1&sk=']

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        next_url = hdoc.select_urls(['//li//a[contains(text(), "Next")]/@href'])
        yield Request(next_url,self.parse,response)

        urls = hdoc.select_urls(['//div[@class="sb_tlst"]//h3//a/@href'], response)
        for url in urls:
            url = xcode(textify(url))
            feed_type = 'travel insurance'
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}

            try:
                IdBing7Spider.db.insert(IdBing7Spider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url), 'feed_type':feed_type}).process()
            except httplib.BadStatusLine:
                continue
        got_page(self.name, response)

