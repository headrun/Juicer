from juicer.utils import *

class Sap(JuicerSpider):
    name = 'sapurls_cache_c'

    def start_requests(self):
        requests = []
        conn = MySQLdb.connect('localhost','root','root','SAP_CACHE')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        print "Came here 01"
        sql = "SELECT pub_id, profile_url FROM sap_urls WHERE is_crawled = 2"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                _id = row[0]
                url = row[1]
                try:
                    upt = "UPDATE sap_urls SET is_crawled = 2 WHERE pub_id = %s" % (_id)
                    cursor.execute(upt)
                except:
                    pass
                r = Request(url, self.parse, None, meta={'_id': _id})
                requests.extend(r)

        except:
            print 'unable to fetch from database'
            pass
        return requests


    def parse(self, response):
        hdoc = HTML(response)

        _id = response.meta['_id']
        out_file = file('/home/headrun/venu/sap_urls_crawled','ab+')
        out_file.write('%s\n' %_id)
        out_file.close()
