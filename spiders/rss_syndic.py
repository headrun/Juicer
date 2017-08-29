import httplib

from juicer.utils import *

class SyndicSpider(JuicerSpider):
    name = 'rss_syndic'
    start_urls = ['http://www.syndic8.com/feedcat.php?Scheme=Syndic8#tabtable'\
                                      'http://www.syndic8.com/feedcat.php?Scheme=DMOZ#tabtable'\
                                      'http://www.syndic8.com/feedcat.php?Scheme=NIF#tabtable'\
                                      'http://www.syndic8.com/feedcat.php?Scheme=NIF_DMOZ#tabtable'\
                                      'http://www.syndic8.com/feedcat.php?Scheme=TX#tabtable'\
                                      'http://www.syndic8.com/feedcat.php?Scheme=seeAlso#tabtable']

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        import pdb;pdb.set_trace()
        got_page(self.name, response)
        urls = hdoc.select_urls(['//li[@class="feedcatlist"]//b//a/@href',\
                                 '//li[@class="feedcatlist"]//a/@href',\
                                 '//table[@class="feedinfotable"]//b[contains(text(),"Feed URL:")]//parent::td//following-sibling::td//a/@href'], response)
        for url in urls:
            url = xcode(textify(url))
            print ">>>>>>>>>>>>", url
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            try:
                SyndicSpider.db.insert(SyndicSpider.db_name, "rss", doc=doc)
                #yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                print 'BadStatusLine error'
                continue

        got_page(self.name, response)

