import httplib

from juicer.utils import *

class NattstadSpider(JuicerSpider):
    name = 'rss_nattstad'
    start_urls = 'http://www.nattstad.se/own_blogg_new.aspx?c=0'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//a[@class="lightUnderlinedBlue"]/@href', response)
        #print "*************************", len(urls)
        #print "???????????????", urls
        for url in urls:
            url = xcode(textify(url))
            #print "________________________", url
            yield Request(url,self.parse_rss,response)

        next_url = hdoc.select_urls('//a[@id="HyperLinkNext"]/@href', response)
        #print "><><><><><><><><", next_url
        yield Request(next_url,self.parse,response)

    def parse_rss(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//img//parent::a/@href[contains(., "visit_blogg")]', response)
        for url in urls:
            url = xcode(textify(url))
            #print ";;;;;;;;;;;;;;;;;;;;;;;;", url
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            #print doc

            try:
                NattstadSpider.db.insert(NattstadSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                #print 'BadStatusLine error'
                continue
        got_page(self.name, response)

