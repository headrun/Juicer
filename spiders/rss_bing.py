from juicer.utils import *
import urllib2
import simplejson
import time
import hashlib

APP_ID = '5B9D31DAB8FD2D83445751CC84F54F480C451C5B'

PATTERN = 'http://api.search.live.net/json.aspx?Query=%s&Version=2.0&AppId=%s&Sources=Web&web.count=%s&web.offset=%s'

db, db_name = get_cursor()

total = 1000000000
per_page = 50

class PyBingSpider(JuicerSpider):
    name = 'pybing'

    def start_requests(self):

        categories = db.find(db_name, "bing_terms", limit=30)
        categories = categories.get("result", [])
        categories = [cat['term'] for cat in categories]
        site_filters = db.find(db_name, "bing_sites", limit=30)
        site_filters = site_filters.get("result", [])
        site_filters = [site['site'] for site in site_filters]
        search_terms = [cat + '%20' + site for cat in categories for site in site_filters]

        requests = []
        for term in search_terms:
            offset = 0
            tm = term.split('%20')
            url = PATTERN % (term, APP_ID, per_page, offset)
            r = Request(url, self.parse, None, meta={'data': {'term': tm[0], 'site': tm[1]}})
            requests.extend(r)

        for cat in categories:
            offset = 0
            url = PATTERN % ('feed:'+cat, APP_ID, per_page, offset)
            r = Request(url, self.parse, None, meta={'data': {'term': 'feed:'+cat, 'site': ''}})
            requests.extend(r)

        self.start_urls = requests
        requests = JuicerSpider.start_requests(self)
        print requests
        return requests

    def parse(self, response):
        got_page(self.name, response)

        hdoc = HTML(response)

        data = urllib2.urlopen(response.url).read()
        data = simplejson.loads(data)
        term = data.get('SearchResponse', {}).get('Query', {}).get('SearchTerms','')
        data = data.get('SearchResponse', {}).get('Web', {})
        total = data.get('Total', 0)
        offset = data.get('Offset', 1000000)
        count = 0
        tm_site = response.meta.get('data', {})
        for result in data.get('Results', []):
            doc = {}
            doc['url'] = result.get('Url', None).encode('utf8')
            doc['term'] = tm_site.get('term', '')
            doc['site'] = tm_site.get('site', '')
            doc['position'] = offset + count
            doc['added_dt'] = time.time()
            doc['url_hash'] = hashlib.md5(doc['url']).hexdigest()
            db.update(db_name, "bing_urls", spec={'url_hash': hashlib.md5(doc['url']).hexdigest()}, doc=doc, upsert=True)
            count = count + 1
        if total>=offset:
            offset += per_page
            url = PATTERN %(term, APP_ID, per_page, offset)
            get_page(self.name, url)

SPIDER = PyBingSpider()
