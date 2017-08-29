from juicer.utils import *
import MySQLdb

class Blogger_Urls(JuicerSpider):
    name = 'blogger_urls_sg_practice'

    def parse(self, response):

        e = e1 = ''
        try: got_page("blogger_urls_sg_practice", response)
        except Exception as e: pass
        try: get_page("blogger_urls_sg_practice", response.url)
        except Exception as e1: pass

        if e: print 'error in got_page>>>>>>', e, '\n'
        if e1: print 'error in get_page>>>', e1, '\n'
        return

