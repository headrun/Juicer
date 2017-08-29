from juicer.utils import *
import urlparse
import pymongo

client = pymongo.Connection("46.4.102.177", 27017)
db = client.wordpress
collection = db.wp_api_feeds

class Botd_Browse(JuicerSpider):
    name = "botd_browse_urls"
    handle_httpstatus_list = [302, 400, 401, 403, 404, 408, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510]

    def parse(self, response):
        hdoc = HTML(response)

        blogs = hdoc.select_urls(['//h4/parent::a/@href|//h4//a/@href'], response)
        netlocs = [urlparse.urlparse(blog).netloc for blog in blogs]

        docs = []
        for net in netlocs:
            doc = {"netloc": net, "is_added" : 0, "added":get_current_timestamp()}
            docs.append(doc)

        try:
            if docs:
                collection.insert(docs, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError as e: print e.message

        got_page(self.name, response)
