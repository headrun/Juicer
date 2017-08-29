import sys
import urllib2, urllib
import time

from cloudlibs import proxy
from juicer.utils import get_current_timestamp

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

def get_results(search_term, customer_name):
    search_term = urllib.quote(search_term)
    print search_term

    db = proxy(DB_HOST, DB_APP_ID, DB_PIPE_ID, DB_PIPE_SECRET)
    db_s = proxy(SEARCH_HOST, SEARCH_APP_ID, SEARCH_PIPE_ID, SEARCH_PIPE_SECRET)

    scroll_id = ''

    prev_max_id = None

    try:
        tot_latest_updated = eval(open('flipkart_rss_max_id').read().strip())
    except IOError:
        tot_latest_updated = {}

    page_index = 1

    latest_updated = float(tot_latest_updated.get(search_term, 0.0))
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
            tot_latest_updated[search_term] = str(results[0]['_source']['updated'])
            f.write('%s' %tot_latest_updated)
            f.close()

        final_data = []
        spec_links = []

        loop_break = False

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
                _data['customer'] = customer_name
                spec_links.append({'link': _result['link']})

                final_data.append(_data)
            else:
                loop_break = True
                break

        if loop_break:
            if final_data:
                db.update(DB_NAME, 'socialdashborad_dataentires', spec=spec_links, doc=final_data, upsert=True)
            break
        else:
            if final_data:
                db.update(DB_NAME, 'socialdashborad_dataentires', spec=spec_links, doc=final_data, upsert=True)

        time.sleep(0.5)
        page_index = page + 1

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
