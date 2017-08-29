import httplib

from juicer.utils import *

class DioenglishSpider(JuicerSpider):
    name = 'rss_dioenglish'
    start_urls = ['http://www.dioenglish.com/network.php?ac=space&view=all' , 'http://www.dioenglish.com/network.php?ac=space&view=online']

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        terminal_url = hdoc.select_urls(['//p[@class="online_icon_p"]//a/@href'], response)
        for url in terminal_url:
            yield Request(url,self.parse_feed,response)

        next_url = hdoc.select_urls('//div[@class="page"]//a[@class="next"]/@href', response)
        yield Request(next_url,self.parse,response)

    def parse_feed(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        '''visitor_url = textify(hdoc.select('//ul[@class="avatar_list"]//li//p//a/@href'))
        for url in visitor_url:
            print "&&&&&&&&&&&&&&&&&&&&", url
            yield Request(url,self.parse_feed,response)
        '''

        feed_id = (response.url).split('?uid=')[-1]

        feed_url = 'http://www.dioenglish.com/rss.php?uid=' + feed_id
        url = xcode(textify(feed_url))
        get_page(self.name, url)
        doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
        #print doc

        try:
            DioenglishSpider.db.insert(DioenglishSpider.db_name, "rss", doc=doc)
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
        except httplib.BadStatusLine:
            print 'BadStatusLine error'
            #continue
        got_page(self.name, response)

