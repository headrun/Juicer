#!/usr/bin/env python

from lxml import html
from lxml.html.clean import clean_html
import time
import datetime
from juicer.utils import *

DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "b9BeD8qTRQlijr8FjXARk8gmmfv14vXI6BXSfRFy"
DB_PIPE_SECRET = "tGLKh0OF6uZQuV50TG2F550tJqOR4h5QCbhzAHzS"

SEARCH_HOST = "http://api.cloudlibs.com/search/"
SEARCH_APP_ID = "4e8d8a01df3cb53978000003"
SEARCH_PIPE_ID = "AAVoqfzbAd8tn9wqRB8MeOPQabTm3ugJKl9P1kys"
SEARCH_PIPE_SECRET = "3WWu22dgx3TXmTcI1GrbVSgSPwy5La4aDQcksVGw"

SETTINGS_FILE = "latest_updated.rss_indexer"

MAX_RECORDS_CRAWL = 1000
MAX_NUM_RECORDS_CRAWL = 10000

def format_time(update):
    update = time.gmtime(float(update))
    return datetime.datetime(*update[:6]).isoformat()

def pull_data(num_records):
    db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)
    search, _ = get_cursor(SEARCH_HOST, SEARCH_PIPE_ID, SEARCH_PIPE_SECRET, SEARCH_APP_ID)

    _records = []
    _ids = []

    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = float(latest_updated)

    except IOError:
        latest_updated = 0.0

    records = db.find("juicerprod", "rss_entries", spec={"_updated": {"$gte":latest_updated}}, sort=[["_updated", 1]], limit=MAX_RECORDS_CRAWL)
    records = records.get("result", [])
    print len(records)
    if records:
        latest_updated = records[-1].get("_updated")
    else:
        return MAX_NUM_RECORDS_CRAWL

    num_records += len(records)

    for record in records:
        """
        {'updated': 978444275.0, 'description': 'FHM Singapore reveals the top 100 sexiest women in the world at St James Power House', 'title': 'FHM 100 Sexiest Women In the World Party', 'author': 'inSing.com', 'link': 'http://www.insing.com/shopping/gallery/fhm-100-sexiest-women-in-the-world-party/id-c66d0300', '_id': 'www.insing.com:9981e0d5eabd5d587549dd8c79719003', 'tags': []}
        """

        try:
            tree = html.fromstring(record.get("description",""))
            tree = clean_html(tree)
            text = tree.text_content()
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            text = record.get("description", "")

        record["description"] = xcode(text)
        record["tags"] = record.get("tags", [])
        record["xtags"] = record.get("xtags", [])
        record["_updated"] = format_time(record["_updated"])

        try:
            record["updated"] = format_time(record["updated"])
        except TypeError, e:
            record["updated"] = 0

        publish = record.get("published", '')
        if publish:
            try:
                record["published"] = format_time(publish)
            except TypeError, e:
                record["published"] = record["updated"]
        else:
            record["published"] = record["updated"]

        _records.append(record)
        _ids.append(record.get("_id"))


    search.index("rss", "item", _records, _ids)
    print 'num', num_records

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

