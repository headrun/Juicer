from juicer.utils import*
from dateutil import parser

class Month(JuicerSpider):
    name = 'month'
    start_url = ['']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select().extract()
        for category in categories:
            if 'http' not in category : category=''+categoru
            yield

