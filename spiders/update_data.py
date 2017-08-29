#!/usr/bin/env python

import time
import datetime
import os
import optparse
from juicer.utils import *

from cloudlibs import proxy


DB_HOST = "http://api.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"

SETTINGS_FILE = "latest_id_user_spider"

MAX_RECORDS_CRAWL = 500

db = proxy(DB_HOST, DB_APP_ID)

def xcode(text, encoding='utf8', mode='ignore'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text

def pull_data():
    try:
        latest_ids = open(SETTINGS_FILE).read().strip()
        latest_ids = eval(latest_ids)

    except IOError:
        latest_ids = {}
    try:
        latest_id = latest_ids.get('angieslist_terminal','000000000000000000000000')
        records = db.find("juicerprod", "datastore", spec={"spider": "angieslist_terminal","_id": {"$gt":latest_id}}, sort=[["_id", 1]], limit=MAX_RECORDS_CRAWL)
    except:
        pull_data()
    records = records.get("result", [])
    for record in records:
        region = record['data']['url']
        region = region.split('/')[5].upper()
        record['data']['region'] = region
        p = db.update("juicerprod", "datastore", spec={"_id" : record['_id']}, doc = record)

    if records:
        latest_id = records[-1].get("_id")
    else:
        return

    latest_ids['angieslist_terminal'] = latest_id
    open(SETTINGS_FILE, "w").write(str(latest_ids))
    return latest_id

if __name__ == "__main__":

    while 1:
        latest_id = pull_data()
        print 'latest_id', latest_id
        if latest_id:
            continue
        else:
            break
