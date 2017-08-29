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

def get_results(search_term):
    search_term = urllib.quote(search_term)

    db = proxy(DB_HOST, DB_APP_ID, DB_PIPE_ID, DB_PIPE_SECRET)

    url = 'https://graph.facebook.com/search?q=%s&limit=100' % (search_term)
    print url


    for page in xrange(1, 1000000):
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
        results = data['data']

        if not results: break

        ids = []
        final_data = []
        _ids = []

        try:
            last_max_id = open('facebook_max_id', 'r').read()
        except IOError:
            last_max_id = '1'

        if page == 1:
            f = open('facebook_max_id', 'w')
            f.write('%s' %results[0]["id"])
            f.close()

        loop_break = False
        for result in results:
            #print repr(result)
            _data = {}
            _data['title'] = result.get('name')

            try:
                _data['description'] = result['message']
            except KeyError:
                description = result.get('caption')
                description = description if description else result.get('description')
                _data['description'] = description

            _data['author'] = result['from']['name']
            _data['created_at'] = result['created_time']
            _data['source_type'] = 'facebook'
            _data['original_data'] = result
            _data['_updated'] = get_current_timestamp()
            _data['fb_id'] = result['id']
            ids.append({'fb_id': result['id']})
            _ids.append(result['id'])

            if last_max_id in _ids:
                loop_break = True
                break
            final_data.append(_data)

        if loop_break:
            if final_data:
                db.update(DB_NAME, 'flipkart_data', spec=ids, doc=final_data, upsert=True)
            break
        else:
            if final_data:
                db.update(DB_NAME, 'flipkart_data', spec=ids, doc=final_data, upsert=True)


        url = data['paging']['next']
        print url
        time.sleep(0.5)

if __name__ == '__main__':

    for term in SEARCH_TERMS:
        print '== ', term
        get_results(term)
