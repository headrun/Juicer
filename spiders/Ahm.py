from juicer.utils import*
from dateutil import parser


class Abplive(JuicerSpider):
    name = 'abplive'
    start_urls = ['http://www.abplive.in/india-news','http://www.abplive.in/world-news','http://www.abplive.in/sports','http://www.abplive.in/lifestyle','http://www.abplive.in/movies','http://www.abplive.in/television','http://www.abplive.in/gadgets','http://www.abplive.in/viral-sach']

    def parse(self,response):
        hdoc = HTML(response)
        links = texify(hdoc.select('//'))
