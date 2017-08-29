from juicer.utils import *
import hashlib
import pymongo

client = pymongo.Connection("46.4.102.177", 27017)
db = client.wordpress
collection = db.wordpress_search_urls

def get_urls():
    alphabets = 'abcdefghijklmnopqrstuvwxyz0123456789'
    urls= []
    for i in alphabets:
        url = 'http://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker=%s'
        urls.append(url %(i))

    return urls

class Wordpress(JuicerSpider):
    name = "wordpress_add_words"
    #start_urls = ['http://www-personal.umich.edu/~jlawler/wordlist']
    start_urls = ['http://www.wordlab.com/archives/company-names-list/']
    #start_urls = get_urls()

    def parse(self, response):
        hdoc = HTML(response)

        #words = response.body.replace('\r', '').split('\n')
        #words = hdoc.select('//div[@class="entry"]//p[3]/text()')
        #words = hdoc.select('//div[@id="mw-content-text"]//a/text()')
        #words = hdoc.select('//div[@class="companies_listing row"]//li//a/text()')
        #words = hdoc.select('//table[@id="main_table_blue"]//td[@align="left"]//a/text()')
        #words = hdoc.select('//table[@class="data1"]//a/text()')
        words = file("/home/headrun/venu/city_names", "r").readlines()


        words = [textify(w).replace('\n','').strip() for w in words if textify(w).replace('\n','').strip() and len(textify(w).replace('\n','').strip()) > 1]
        words = [w.lower().replace(' ', '+') for w in words]
        words = list(set(words))

        print len(words)
        docs = []
        for word in words:

            urls = ["http://en.search.wordpress.com/?q=%s", 'http://en.search.wordpress.com/?q=%s&page=2',
                    "http://en.search.wordpress.com/?q=%s&page=3", "http://en.search.wordpress.com/?q=%s&page=4",
                    "http://en.search.wordpress.com/?q=%s&page=5", "http://en.search.wordpress.com/?q=%s&s=date&t=post",
                    "http://en.search.wordpress.com/?q=%s&s=date&t=post&page=2", "http://en.search.wordpress.com/?q=%s&s=date&t=post&page=3",
                    "http://en.search.wordpress.com/?q=%s&s=date&t=post&page=4", "http://en.search.wordpress.com/?q=%s&s=date&t=post&page=5"
                ]

            urls = [url%(word) for url in urls]

            for url in urls:
                try:
                    url_hash = hashlib.md5(url).hexdigest()
                except: continue
                doc = {"url_hash" : url_hash, "url" : url, "is_crawled" : 0}

                docs.append(doc)

            if len(docs) % 20000 == 0:
                try:
                    if docs:
                        collection.insert(docs, continue_on_error=True)
                except pymongo.errors.DuplicateKeyError as e: print e.message
                del docs[:]

        try:
            if docs:
                collection.insert(docs, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError as e: print e.message
        del docs[:]



