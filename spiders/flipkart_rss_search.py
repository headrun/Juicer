import sys
import urllib2, urllib
import simplejson
import time
import random
import requests

from cloudlibs import proxy
from juicer.utils import get_current_timestamp

USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
                    'Mozilla/5.0 (Windows NT 6.2; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
                    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0',
                    'Mozilla/5.0 (U; Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101128 Firefox/4.0b8pre',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20100101 Firefox/4.0b7',
                    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52',
                    'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
                    'Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01',
                    'Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; pl) Opera 11.00',
                    'Opera/9.80 (Windows NT 5.1; U; pl) Presto/2.6.30 Version/10.62',
                    'Opera/9.80 (X11; Linux x86_64; U; it) Presto/2.2.15 Version/10.10',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
                    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
                    'Mozilla/5.0 (X11; CrOS i686 1193.158.0) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.8',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; th-th) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ko-kr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-gb) AppleWebKit/528.10+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2']

PROXIES_LIST = ['%s:3279' % ip.strip() for ip in urllib.urlopen('http://hosting.cloudlibs.com/static/misc/juicer_proxy_ips')]

SEARCH_TERMS = ['Flipkart']
MAX_RECORDS_CRAWL = 1000

DB_NAME = "juicerprod"
DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "b9BeD8qTRQlijr8FjXARk8gmmfv14vXI6BXSfRFy"
DB_PIPE_SECRET = "tGLKh0OF6uZQuV50TG2F550tJqOR4h5QCbhzAHzS"

SEARCH_HOST = "http://api.cloudlibs.com/search/"
SEARCH_APP_ID = "4e8d8a01df3cb53978000003"
SEARCH_PIPE_ID = "AAVoqfzbAd8tn9wqRB8MeOPQabTm3ugJKl9P1kys"
SEARCH_PIPE_SECRET = "3WWu22dgx3TXmTcI1GrbVSgSPwy5La4aDQcksVGw"

def get_results(search_term):
    search_term = urllib.quote(search_term)

    db = proxy(DB_HOST, DB_APP_ID, DB_PIPE_ID, DB_PIPE_SECRET)
    db_s = proxy(SEARCH_HOST, SEARCH_APP_ID, SEARCH_PIPE_ID, SEARCH_PIPE_SECRET)

    scroll_id = ''

    prev_max_id = None

    try:
        latest_updated = float(open('flipkart_rss_max_id').read().strip())
    except IOError:
        latest_updated = 0.0

    page_index = 1

    for page in xrange(1, 1000000):

        if scroll_id:
            try:
                records = db_s.search_scroll(scroll_id = scroll_id , scroll_timeout = "10m")
            except:
                time.sleep(3)
                print 'except'
                continue
        else:
            try:
                records = db_s.search(indexes = "rss" , doc_types = "item", query =  {"query": {"query_string": {"query": search_term, "fields": ["title","description", "link"] , "use_dis_max": True}}, "sort":[{"updated":{"order":"desc"}}], "size":MAX_RECORDS_CRAWL }, query_params={"scroll": "15m"})
            except:
                time.sleep(3)
                print 'except'
                continue

        scroll_id =  records.get("result", []).get("_scroll_id", [])
        results = records.get("result", []).get("hits", []).get("hits", [])

        if not results: break

        if page_index == 1:
            f = open('flipkart_rss_max_id', 'w')
            f.write('%s' %results[0]['_source']['updated'])
            f.close()

        final_data = []
        spec_links = []

        loop_break = False
        print len(results)

        for result in results:
            _result = result['_source']
            result.pop('_index')
            if  _result['updated'] > latest_updated:
                _data = {}
                _data['title'] = _result['title']
                _data['description'] = _result['description']
                _data['author'] = _result['author']
                _data['created_at'] = time.ctime(_result['published'])
                _data['source_type'] = 'rss'
                _data['original_data'] = result
                _data['_updated'] = get_current_timestamp()
                _data['link'] = _result['link']
                spec_links.append({'link': _result['link']})

                final_data.append(_data)
            else:
                loop_break = True
                break

        if loop_break:
            if final_data:
                db.update(DB_NAME, 'flipkart_data', spec=spec_links, doc=final_data, upsert=True)
            break
        else:
            if final_data:
                db.update(DB_NAME, 'flipkart_data', spec=spec_links, doc=final_data, upsert=True)

        time.sleep(0.5)
        page_index = page

if __name__ == '__main__':

    for term in SEARCH_TERMS:
        print '== ', term
        get_results(term)
