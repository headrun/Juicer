from juicer.utils import *
from dateutil import parser
import ast

class NatlibNz(JuicerSpider):
    name = 'natlib'
    start_urls = 'http://natlib.govt.nz/'


    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
