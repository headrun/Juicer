from juicer.utils import *
from lxml import etree

class Temp(JuicerSpider):
    name = "temp_script"

    def start_requests(self):
        requests = []

        url = 'http://content5.flixster.com/feeds/private/us/2_MOVIE_FEED.xml'

        hdrs = {"Authorization" : "Basic cm92aTpRSi5xNSI+Tg=="}

        r = Request(url, self.parse, None, headers=hdrs)

        requests.extend(r)

        return requests

    def parse(self, response):

        response_file = "xml_data"

        out_file = open(response_file, "w")
        out_file.write('%s' %(response.body))
        out_file.flush()

        context = etree.iterparse(response_file, tag='movie')

        movie_ids, titles, count = [], [], 0

        for event, elem in context:
            movie_ids.append(elem.xpath("@id"))
            titles.append(elem.xpath("title/text()"))
            count += 1

        print count
        print "movie_id >>>", movie_ids[0]
        print "title >>>>>", titles[0]
