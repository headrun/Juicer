from juicer.utils import *
from dateutil import parser

class WhirlpoolForum(JuicerSpider):
    name = 'whirlpool_forum'
    start_urls = ['http://forums.whirlpool.net.au/forum/123']

    import pdb;pdb.set_trace()
    def parse(self,response):
        hdoc = HTML(response)
        print "sindhu"
        import pdb;pdb.set_trace()
