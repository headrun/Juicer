import httplib

from juicer.utils import *

class QingTerminalSpider(JuicerSpider):
    name = 'qing_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        feed_url = get_request_url(response).split('/')[-1]
        url = 'http://qing.weibo.com/rss/' + feed_url

        doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
        #print doc

        try:
            QingTerminalSpider.db.insert(QingTerminalSpider.db_name, "rss", doc=doc)
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
        except httplib.BadStatusLine:
            print 'BadStatusLine error'
            #continue

        atricle_url = hdoc.select('//div[@class="pubFeedAttr"]//a[@class="more"]/@href')
        for url in atricle_url:
            url = textify(url)
            yield Request(url, self.parse_article, response)

    def parse_article(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select('//ul[@class="avatarList clearfix"]//li//a/@href')
        for url in urls:
            url = textify(url)
            get_page('qing_terminal', url)
