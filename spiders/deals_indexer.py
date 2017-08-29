#!/usr/bin/env python

import time
import datetime
from juicer.utils import *

from cloudlibs import proxy

DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "b9BeD8qTRQlijr8FjXARk8gmmfv14vXI6BXSfRFy"
DB_PIPE_SECRET = "tGLKh0OF6uZQuV50TG2F550tJqOR4h5QCbhzAHzS"

SEARCH_HOST = "http://api.cloudlibs.com/search/"
SEARCH_APP_ID = "4f62e204934c2b0c35000000"

SETTINGS_FILE = "latest_updated.deals_indexer"

MAX_RECORDS_CRAWL = 1000

def pull_data():
    dbname = "juicerprod"
    db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)
    search = proxy(SEARCH_HOST, SEARCH_APP_ID)
    spidernames = ['crazeal_terminal', 'dealsandyou_terminal', 'snapdeal_terminal', 'mydala_terminal', 'koovs_terminal']

    _records = []
    _ids = []

    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = eval(latest_updated)

    except IOError:
        latest_updated = {}

    for spidername in spidernames:
        latest_spider = latest_updated.get(spidername, 0.0)
        records = db.find(dbname, "datastore", spec={"spider": spidername, "updated": {"$gte": latest_spider}}, sort=[["updated", -1]],
                    limit=MAX_RECORDS_CRAWL)
        records = records.get("result", [])
        print "Count<><><><><>:", len(records)

        if records:
            latest_spider = records[-1]['updated']

        for record in records:
            if not isinstance(record["data"]["discount"], int):
                if record["data"]["discount"] is not '':
                    if 'Rs' in record["data"]["discount"]:
                        print "::::::::::::::::::", record["data"]["url"]
                        record["data"]["discount"] = int(float(record["data"]["discount"].split(' ')[-1].replace('%', '')))
                        print "<><><><><><><>", record["data"]["discount"]
                    else:
                        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", record["data"]["url"]
                        record["data"]["discount"] = int(float(record["data"]["discount"].replace('%', '')))
                        print "<><><>><><>>>", record["data"]["discount"]
                else:
                    record["data"]["discount"] = 0
            record["updated"] = get_datetime(record["updated"]).isoformat()
            record["added"] = get_datetime(record["added"]).isoformat()
            print "record :::::", record
            _records.append(record)
            _ids.append(record.get("_id"))
            #search.index("deals", "item", record, record.get('_id'))

        search.index("deals", "item", _records, _ids)

        if records:
            latest_updated[spidername] = latest_spider
            open(SETTINGS_FILE, "w").write(str(latest_updated))


if __name__ == "__main__":
    pull_data()
