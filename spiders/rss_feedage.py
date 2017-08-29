import httplib
from itertools import chain, combinations
import string

from juicer.utils import *

SETTINGS_FILE = "last_updated"
MAX_RECORDS_TRANSFER = 500

def gen_search_urls():
    ngrams = [''.join(x) for i in [2, 3] for x in combinations(string.lowercase, i)]
    search_url_pattern = 'http://www.feedage.com/adv_search.php?t=%(term)s&at=&et=&nt=&language=&media_type=&st=y&sd=y&sk=y&su=y&sb=%(sort)s&Submit=Search'
    urls = [search_url_pattern % locals() for term in ngrams for sort in xrange(1, 7)]
    return urls

START_URLS = ['http://www.feedage.com/categories/']
START_URLS.extend(gen_search_urls())

class FeedageSpider(JuicerSpider):
    name = 'rss_feedage'
    start_urls = START_URLS

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls('//td[@class="category_cell"]/a/@href', response)
        urls = [u.rsplit('/', 1)[0] for u in urls]
        urls = [[(u + '/' + str(i)) for i in xrange(1, 7)] for u in urls]
        urls = list(chain(*urls))

        for url in urls:
            get_page(self.name, url)

        for node in hdoc.select('//div[@class="feedurl"]'):
            #sk = textify(node.select('./parent::td/parent::tr/preceding-sibling::tr[3]/td/a/@href')).split('/')[2]
            url = xcode(textify(node))
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            try:
                FeedageSpider.db.insert(FeedageSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                # ignoreing error. needs to be debugged in cloudlibs dbservice
                print 'BadStatusLine error'
                continue

        urls = hdoc.select_urls('//a/img[contains(@alt,"Next")]/parent::a/@href', response)
        for url in urls:
            get_page(self.name, url)
