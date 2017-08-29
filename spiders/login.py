from juicer.utils import *
from scrapy.http import FormRequest

class LogIn(JuicerSpider):
    name = "login"
    start_urls = ['https://www.patientslikeme.com']

    def parse(self,response):
        hdoc = HTML(response)
        auth = textify(hdoc.select('//meta[@name="csrf-token"]/@content'))
        import pdb;pdb.set_trace()
        formdata={'utf8':'\xe2\x9c\x93','authenticity_token':str(auth),'userlogin[login]':'kiran_moka','userlogin[password]':'kiRan_29','commit':'Sign in','walgreens_continue_url':''}
        yield FormRequest('https://www.patientslikeme.com/login',self.parse_login,formdata=formdata,meta = {'dont_redirect': False,'handle_httpstatus_list': [302]})

    def parse_login(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        url = textify(hdoc.select('//a/@href'))
        url = 'https://www.patientslikeme.com/forum/plm/topics/135875'
        yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        import pdb;pdb.set_trace()
