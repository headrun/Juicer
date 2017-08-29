#!/usr/bin/env python

import time
import datetime
from juicer.utils import *
from cloudlibs import proxy

DB_HOST = "http://alpha.cloudlibs.com/db/"
DB_APP_ID = "4e6c4df97564575f12000003"
DB_PIPE_ID = "eJER3gRDuxPnxqcfHZvdzkQhfo8fwnj9Bnz0V1kk"
DB_PIPE_SECRET = "nPfMaxnbcCa0XrIc3Rh0V58BfAgeHZAZyxBE7H8i"

SEARCH_HOST = "http://alpha.cloudlibs.com/search/"
SEARCH_APP_ID = "4ef95d007564576d55000000"
SEARCH_PIPE_ID = "JPK0GHftiQ4UUaP11iffoVotQ8kQrOTOtWWB52Nz"
SEARCH_PIPE_SECRET = "kd0fDRGluNsYlGpC79aVto6EWqltztWDY0I5ndQf"

COUNTER_HOST = "http://alpha.cloudlibs.com/counter/"
COUNTER_APP_ID = "4f0a9abe75645736de000000"

SETTINGS_FILE = "latest_updated.spider_indexer"

MAX_RECORDS_CRAWL = 1000

def pull_data():
    dbname = "juicerprod"
    db, _ = get_cursor(DB_HOST, DB_PIPE_ID, DB_PIPE_SECRET, DB_APP_ID)
    search = proxy(SEARCH_HOST, SEARCH_APP_ID)
    counter = proxy(COUNTER_HOST, COUNTER_APP_ID)
    count_spiders = {}
    count_search = {}

    spidernames = [ 'amazoninstantvideos_terminal', 'holidaylettings_terminal', 'edmunds_terminal', 'taggle_terminal', 'paulweiss', 'imdb_terminal', 'rulist', 'myntra', 'holidayrentals_terminal', 'toptable_terminal', 'meijer_terminal', 'westelm_terminal', 'purelandsupply_terminal', 'trulia_terminal', 'amazonapps_terminal', 'ownersdirect_terminal', 'menupages_terminal', 'beautylish_terminal', 'reviewcentre_terminal', 'etsy_terminal', 'rei_terminal', 'thecatholicdirectory_terminal', 'truelocal_terminal', 'movoto_terminal', 'walgreens_terminal', 'tripadvisor_terminal', 'gnavi_terminal', 'nextagtravel_terminal', 'qype_terminal', 'stevemadden_terminal', 'allmenus_terminal', 'ladyfootlocker_terminal', 'bulbsolutions_terminal', 'dealerdex_terminal', 'boattrader_terminal', 'openlibrary_terminal', 'yebhi',  'yipit_terminal', 'drugstore_terminal', 'yellowpages_terminal', 'dealerrater_terminal', 'dsg_terminal', 'groupon']


    try:
        latest_updated = open(SETTINGS_FILE).read().strip()
        latest_updated = eval(latest_updated)

    except IOError:
        latest_updated = {}

    for spidername in spidernames:
        print spidername
        latest_spider = latest_updated.get(spidername, 0.0)
        try:
            records = db.find(dbname, "datastore", spec={"spider": spidername, "updated": {"$gte": latest_spider}}, sort=[["updated", -1]],
                        limit=MAX_RECORDS_CRAWL)
        except:
            continue
        records = records.get("result", [])
        name = 'db:' + spidername
        count_spiders[name] = len(records)
        print len(records)
        if records:
            latest_spider = records[-1]['updated']

        count = 0
        for record in records:
            count = count + 1
            record["updated"] = get_datetime(record["updated"]).isoformat()
            record["added"] = get_datetime(record["added"]).isoformat()
            search.index(record, "spider", "item", record.get("_id"))

        sname = 'search:' + spidername
        count_search[sname] = count

        if records:
            latest_updated[spidername] = latest_spider
            open(SETTINGS_FILE, "w").write(str(latest_updated))

        time.sleep(30)

    print count_search, count_spiders
    counter.bulk.update(count_search)
    counter.bulk.update(count_spiders)


if __name__ == "__main__":
    pull_data()
