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

SEARCH_TERMS = ['flipkart']

DB_NAME = "juicerprod"
DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "b9BeD8qTRQlijr8FjXARk8gmmfv14vXI6BXSfRFy"
DB_PIPE_SECRET = "tGLKh0OF6uZQuV50TG2F550tJqOR4h5QCbhzAHzS"

def get_results(search_term, customer_name):
    search_term = urllib.quote(search_term)
    geocode = '-23.88583769986199,118.828125,4000km'

    db = proxy(DB_HOST, DB_APP_ID, DB_PIPE_ID, DB_PIPE_SECRET)

    url = 'http://search.twitter.com/search.json?q=%s&rpp=2000' % (search_term)
    print url


    prev_max_id = None
    for page in xrange(1, 1000000):
        ids = set()
        try:
            data = requests.get(url, proxies={'http': random.choice(PROXIES_LIST)}, headers={'User-Agent': random.choice(USER_AGENT_LIST)}, timeout=30)
        except requests.exceptions.ConnectionError:
            print '@@', 'connection failed'
            continue
        except requests.exceptions.Timeout:
            print '@@', 'connection timedout'
            continue

        if data.status_code != 200:
            print '@@ ', data.status_code
            time.sleep(10)
            continue

        data = simplejson.loads(data.text)
        results = data['results']

        if not results: break

        try:
            last_max_id = int(open('twitter_max_id', 'r').read())
        except IOError:
            last_max_id = 1

        if page == 1:
            f = open('twitter_max_id', 'w')
            f.write('%s' %results[0]["id"])
            f.close()

        final_data = []
        spec_ids = []

        loop_break = False

        for result in results:
            _id = result["id"]
            _data = {}
            _data['title'] = ''
            _data['description'] = result['text']
            _data['author'] = result['from_user_name']
            _data['created_at'] = result['created_at']
            _data['source_type'] = 'twitter'
            _data['original_data'] = result
            _data['_updated'] = get_current_timestamp()
            _data['tweet_id'] = result['id_str']
            _data['customer'] = customer_name
            spec_ids.append({'tweet_id': result['id_str']})

            ids.add(_id)
            if last_max_id in ids:
                loop_break = True
                break
            final_data.append(_data)
        max_id = _id

        if loop_break:
            if final_data:
                db.update(DB_NAME, 'socialdashborad_dataentires', spec=spec_ids, doc=final_data, upsert=True)
                break
        else:
            if final_data:
                db.update(DB_NAME, 'socialdashborad_dataentires', spec=spec_ids, doc=final_data, upsert=True)

        if max_id == prev_max_id:
            break

        print result['created_at'], len(ids)

        url = 'http://search.twitter.com/search.json?rpp=2000&q=%s&max_id=%s' % (\
                search_term, _id)
        print url
        time.sleep(0.5)
        prev_max_id = max_id

if __name__ == '__main__':

    data = sys.argv[1]
    customers = eval(data)

    for customer in customers:
        search_terms = customer.get('keywords')
        customer_name = customer.get('customer_name')

        if isinstance(search_terms, str):
            get_results(search_terms, customer_name)
        elif isinstance(search_terms, list):
            for term in search_terms:
                get_results(term, customer_name)
        else:
            print 'Unsupported keywords type expected str or list but got %s type' %type(search_terms)