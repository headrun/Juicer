#!/usr/bin/env python

from lxml import html
from lxml.html.clean import clean_html
import time
import datetime
from juicer.utils import *
import csv
import shutil
import os
import sys

DB_HOST = "http://www.cloudlibs.com/db/"
DB_APP_ID = "4e8d4f84df3cb5386a000005"
DB_PIPE_ID = "sCQTKgyx2iPpIgEiMoUHJFcqS2WFTNmKeBpNiyjl"
DB_PIPE_SECRET = "XWSvckyhfKuqi7FLlXA3LH8Gu6ImJKRbBTX34Q4z"

SEARCH_HOST = "http://www.cloudlibs.com/search/"
SEARCH_APP_ID = "4e8d8a01df3cb53978000003"
SEARCH_PIPE_ID = "AAVoqfzbAd8tn9wqRB8MeOPQabTm3ugJKl9P1kys"
SEARCH_PIPE_SECRET = "3WWu22dgx3TXmTcI1GrbVSgSPwy5La4aDQcksVGw"

SETTINGS_FILE = "latest_id.thoughtbuzz"

MAX_RECORDS_CRAWL = 5000

#db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)


def pull_data(csvWriter):
    #thought_file = open('thought_buzz.data', 'a+')
    try:
        latest_id = open(SETTINGS_FILE).read().strip()
    except IOError:
        latest_id = '000000000000000000000000'
    print latest_id
    #records = db.find("juicerprod", "rss_entries", spec={"_id": {"$gte":latest_id}}, sort=[["_id", 1]], limit=MAX_RECORDS_CRAWL)
    try:
        records = db.find("juicerprod", "rss_entries", spec={"_id": {"$gt":latest_id}, "$or":[{'xtags':'vietnam_country_manual_parent'}, {'xtags':'malaysia_country_manual_parent'}, {'xtags':'philippines_country_manual_parent'}, {'xtags': 'thailand_country_manual_parent'}, {'xtags': 'indonesia_country_manual_parent'}, {'xtags':'china_country_manual_parent'}]}, sort=[["_id", 1]], limit=MAX_RECORDS_CRAWL)
    except:
        return latest_id
    records = records.get("result", [])
    print len(records)
    if not records:
        open(SETTINGS_FILE, "w").write(str(latest_id))
        done_fname = '%s_%s.csv' %(dump_fname, int(time.time()))
        shutil.move(dump_fname, done_fname)
        return 
    if records:
        latest_id = records[-1].get("_id")

    for record in records:
        try:
            tree = html.fromstring(record.get("description",""))
            tree = clean_html(tree)
            text = tree.text_content()
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            text = record.get("description", "")

        doc = {}
        text = xcode(text)
        text = ' '.join(text.split())
        doc['title'] = xcode(record.get('title', ''))
        doc['description'] = text
        doc['link'] = xcode(record.get('link', ''))
        doc['updated'] = record.get('updated', '')
        doc['tags'] = record.get('tags', '')
        tag = ''
        if doc['tags']:
            tag = xcode(', '.join(doc['tags']))
            #for tagi in doc['tags']: tag = tag + ',' + xcode(tagi)
        xtag = record.get('xtags')
        xtag = xtag[0]
        doc['country'] = xtag.split("_")[0]
        doc['_id'] = record.get('_id', '')
        csvWriter.writerow([doc["_id"], doc["title"], doc["description"], doc["link"], doc["country"], tag, doc["updated"]])
    open(SETTINGS_FILE, "w").write(str(latest_id))
    return latest_id

if __name__=="__main__":
    global db
    db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)
    dump_dir = sys.argv[1]

    dump_fname = os.path.join(dump_dir, 'thoughtbuzz')
    csvWriter = csv.writer(open(dump_fname, 'wb'), delimiter='\t')
    csvWriter.writerow(["_id", "title", "description", "link", "country", "tags", "updated"])
    while 1:
        latest_id = pull_data(csvWriter)
	if latest_id:
	    continue
	else:
	    break
