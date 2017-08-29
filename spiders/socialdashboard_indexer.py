#!/usr/bin/env python
import AlchemyAPI
from lxml import html
from lxml.html.clean import clean_html
from dateutil import parser
from juicer.utils import *

from cloudlibs.utils import *

DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "b9BeD8qTRQlijr8FjXARk8gmmfv14vXI6BXSfRFy"
DB_PIPE_SECRET = "tGLKh0OF6uZQuV50TG2F550tJqOR4h5QCbhzAHzS"

SEARCH_HOST = "http://api.cloudlibs.com/search/"
SEARCH_APP_ID = "506e75a53351d527b5000000"
SEARCH_PIPE_ID = "AAVoqfzbAd8tn9wqRB8MeOPQabTm3ugJKl9P1kys"
SEARCH_PIPE_SECRET = "3WWu22dgx3TXmTcI1GrbVSgSPwy5La4aDQcksVGw"

SETTINGS_FILE = "latest_updated.socialdashboard_indexer"

MAX_RECORDS_CRAWL = 1000
MAX_NUM_RECORDS_CRAWL = 1000

k = Counter()
k.statsd.host = 'stats.api.cloudlibs.com'

def format_time(update):
    return parser.parse(update).isoformat()

def pull_data(num_records):
    db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)
    search, _ = get_cursor(SEARCH_HOST, SEARCH_PIPE_ID, SEARCH_PIPE_SECRET, SEARCH_APP_ID)

    _records = []
    _ids = []
    db_records = []
    db_ids = []

    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = float(latest_updated)

    except IOError:
        latest_updated = 0.0

    records = db.find("juicerprod", "socialdashborad_dataentires", spec={"_updated": {"$gt":latest_updated}}, sort=[["_updated", 1]], limit=MAX_RECORDS_CRAWL)
    records = records.get("result", [])
    k.statsd.update_stats('scripts.flipkart_indexer.num_records_from_datastore', len(records))
    print len(records)
    if records:
        latest_updated = records[-1].get("_updated")
    else:
        return MAX_NUM_RECORDS_CRAWL

    alchemyObj = AlchemyAPI.AlchemyAPI()
    alchemyObj.loadAPIKey("7f75766b9bc3722dca1411d8dd485c08173b5026");
    eparams = AlchemyAPI.AlchemyAPI_NamedEntityParams()
    eparams.setOutputMode('json')

    num_records += len(records)
    print "********************", num_records

    for record in records:
        """
        {'updated': 978444275.0, 'description': 'FHM Singapore reveals the top 100 sexiest women in the world at St James Power House', 'title': 'FHM 100 Sexiest Women In the World Party', 'author': 'inSing.com', 'link': 'http://www.insing.com/shopping/gallery/fhm-100-sexiest-women-in-the-world-party/id-c66d0300', '_id': 'www.insing.com:9981e0d5eabd5d587549dd8c79719003', 'tags': []}
        """

        _record = record
        try:
            tree = html.fromstring(record.get("description",""))
            tree = clean_html(tree)
            text = tree.text_content()
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            text = record.get("description", "")

        record["description"] = xcode(text)
        record["created_at"] = format_time(record["created_at"])

        if record['source_type'] == 'rss':
            record['link'] = record['original_data']['_source']['link']
        elif record['source_type'] == 'facebook':
            record['link'] = record['original_data'].get('link')
            record['original_data'].pop('id')
        elif record['source_type'] == 'twitter':
            record['link'] = 'https://twitter.com/%s/status/%s' %(record['original_data']['from_user'], record['original_data']['id_str'])
        else:
            pass


        description = record['description']
        if description and len(description) > 5:

            s_result = eval(alchemyObj.TextGetTextSentiment(record['description'], eparams))
            status = s_result['status']

            if status == 'OK':
                record['sentiment'] = s_result['docSentiment']['type']
                _record['sentiment'] = s_result['docSentiment']['type']
            else:
                record['sentiment'] = 'neutral'
                _record['sentiment'] = 'neutral'
        else:
            record['sentiment'] = 'neutral'
            _record['sentiment'] = 'neutral'

        _records.append(record)
        db_records.append(_record)
        _ids.append(record.get("_id"))
        db_ids.append({'_id':record.get("_id")})

    db.update('juicerprod', 'socialdashborad_dataentires', spec=db_ids, doc=db_records)
    search.index("socialdashboard", "item", _records, _ids)
    k.statsd.update_stats('scripts.flipkart_indexer.num_records_indexed_search', len(records))
    print 'num', num_records, latest_updated, len(_records)

    open(SETTINGS_FILE, "w").write(str(latest_updated))

    return num_records

if __name__=="__main__":
    num_records = 0
    while(1):
        num_records = pull_data(num_records)
        if num_records< MAX_NUM_RECORDS_CRAWL:
            continue
        else:
            break

