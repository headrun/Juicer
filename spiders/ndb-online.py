from juicer.utils import*
from dateutil import parser

class NdbonlinePh(JuicerSpider):
    name = 'ndb-online'
    start_urls = ['http://www.ndb-online.com/', 'http://www.ndb-online.com/negros-occidental']
