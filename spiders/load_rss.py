import glob
import sys

from os import rename
from juicer.utils import *


def main(argv):

    cutoff_time = argv

    db,name = get_cursor()
    rss_table = db.find("juicerprod", "rss")

    list_of_files = glob.glob("/tmp/rss*.unprocessed")

    for i in list_of_files:
        file_time = re.findall(r'rss_urls_(\d+).unprocessed', i)

        if file_time[0] > cutoff_time:
            file_name = "/tmp/rss_urls_%s.unprocessed" %(file_time[0])
            rss_file = file(file_name, "r+")
            lines = rss_file.readlines()

            for line in lines:
                xtags = []
                feed_url = re.findall(r'(.*)\t\w+\t.*\t', line)
                _id = re.findall(r'.*\t(.*)\t.*\t', line)
                source_type = re.findall(r'.*\t.*\t(.*)\t.*', line)
                country = re.findall(r'.*\t.*\t.*\t(.*)', line)
                feed_url, _id, source_type, country = line.split("\t")
                source_type = source_type +"_sourcetype_manual"
                country = country + "_country_manual"
                xtags.append(source_type)
                xtags.append(country)
                url_hash = md5(feed_url)
                url_check = db.find("juicerprod", "rss" ,spec={'url_hash' : url_hash})

                if not url_check['result']:
                    doc = {"domain_id": _id, "next_run": 0, "url_hash": md5(feed_url),'url': feed_url, 'last_run': 0 , 'xtags': xtags}
                    db.insert("juicerprod", "rss_pending_verification", doc)

        rename(file_name, (file_name[:24])+".processed")

if __name__ == "__main__":
    main(sys.argv[1:])

