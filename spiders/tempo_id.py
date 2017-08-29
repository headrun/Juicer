from juicer.utils import*
from dateutil.utils parser

class Tempo_ID(JuicerSpider):
    name= 'tempo_id'
    start_urls = ['https://www.tempo.co/']

    def parse(self,response):
        hdoc = HTML(response)

