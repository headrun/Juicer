from juicer.utils import *

class SampleAlexa(JuicerSpider):
    name = 'sample_alexa'
    start_urls = ['http://awis.amazonaws.com/?AWSAccessKeyId=AKIAJSFJSHY3WVKBFQDQ&Action=TrafficHistory&ResponseGroup=History&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2016-07-18T14%3A07%3A19.340136&Url=www.aricent.com&Signature=FUAh43EXDmUmpAG1bh5cGyHfea2nuQ4XlWhgJqCrpNA%3D']
    #start_urls = ['http://stackoverflow.com/questions/12254740/scrapy-htmlxpathselector']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
