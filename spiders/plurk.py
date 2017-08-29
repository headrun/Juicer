import oauth2 as oauth
import simplejson
from pprint import pprint
from cloudlibs import proxy
import sys 
import time

API_KEY = 'kank1MbqLOWM'
API_SECRET = 'ccheKxSDGnJZnkBj3YmhC3GEd3LzQSW4'

DB_HOST = "http://www.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"

SETTINGS_FILE = "latest_updated.plurk_search"

_client = oauth.Client()

_consumer = oauth.Consumer(API_KEY, API_SECRET)

def pull_data(search_word, offset, latest):

    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = eval(latest_updated)
    except IOError:
        latest_updated = {}
    print latest_updated

    query = 'query=' + search_word + '&offset=' + str(offset)
    print query
    headers, resp = _client.request("http://www.plurk.com/APP/PlurkSearch/search", 'POST', query, {}, consumer=_consumer)
    true = True
    null = ''
    false = False
    resp = eval(resp)
    plurks = resp.get('plurks')

    latest_offset = latest_updated.get(search_word, 0)

    if not offset :
        latest = plurks[0]['plurk_id']
    for plurk in plurks:
        print plurk.get('plurk_id')
        doc = {}
        data = {}
        data['replurkers_count'] = plurk.get('replurkers_count', '')
        data['replurkable'] = plurk.get('replurkable', '')
        data['favorite_count'] = plurk.get('favorite_count', '')
        data['is_unread'] = plurk.get('is_unread', '')
        data['favorers'] = plurk.get('favorers', '')
        data['user_id'] = plurk.get('user_id', '')
        data['plurk_type'] = plurk.get('plurk_type', '')
        data['replurked'] = plurk.get('replurked','')
        data['content'] = plurk.get('content', '')
        data['qualifier_translated'] = plurk.get('qualifier_translated', '')
        data['owner_id'] = plurk.get('owner_id', '')
        data['responses_seen'] = plurk.get('responses_seen', '')
        data['qualifier'] = plurk.get('qualifier', '')
        data['plurk_id'] = plurk.get('plurk_id', '')
        data['response_count'] = plurk.get('response_count', '')
        data['limited_to'] = plurk.get('limited_to', '')
        data['no_comments'] = plurk.get('no_comments', '')
        data['posted'] = plurk.get('posted', '')
        data['lang'] = plurk.get('lang', '')
        data['content_raw'] = plurk.get('content_raw', '')
        data['replurkers'] = plurk.get('replurkers', '')
        data['favorite'] = plurk.get('favorite', '')
        data['replurker_id'] = plurk.get('replurker_id', '')

        doc['spider'] = 'plurk_search'
        doc['sk'] = data['plurk_id']
        doc['added'] = time.time()
        doc['updated'] = time.time()
        doc['data'] = data
        if doc['sk'] > latest_offset:
            db.insert('juicerprod', 'datastore', doc=doc)

    if plurks and latest_offset < plurks[-1]['plurk_id']:
        return plurks[-1]['plurk_id'], latest
    else:
        return '', latest

if __name__=="__main__":
    global db
    db = proxy(DB_HOST, DB_APP_ID)
    search_file = sys.argv[1]
    fp = open(search_file, 'r')
    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = eval(latest_updated)
    except IOError:
        latest_updated = {}


    for search_word in fp:
        offset = ''
        latest = ''
        search_word = search_word.strip()
        while(1):
            offset, latest= pull_data(search_word, offset, latest)
            if offset:
                continue
            else:
                if latest:
                    latest_updated[search_word] = latest
                    open(SETTINGS_FILE, "w").write(str(latest_updated))
                break
