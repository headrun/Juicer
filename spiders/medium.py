from juicer.utils import *
from lxml import etree

class Medium(JuicerSpider):
    name = "medium"

    def start_requests(self):
        requests = []

        url = 'https://medium.com/@raytirado/follow-list?listType=following&page=0'

        hdrs = {"X-Obvious-CID" : "web", "X-XSRF-Token" : 1, "Content-Type":"application/json", "Accept":"application/json", "Accept-Encoding":"gzip, deflate", "Accept-Language":"en-US,en;q=0.5"}

        r = Request(url, self.parse, None, headers=hdrs)

        requests.extend(r)

        return requests

    def parse(self, response):

        #import pdb;pdb.set_trace()
        response_file = "xml_data"

        out_file = open(response_file, "w")
        out_file.write('%s' %(response.body))
        out_file.flush()


