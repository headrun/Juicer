from juicer.utils import*
from dateutil import parser

class Arcgames(JuicerSpider):
    name = 'forum_arcgames'
    start_urls = ['https://www.arcgames.com/en/forums/blacklightretribution']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

