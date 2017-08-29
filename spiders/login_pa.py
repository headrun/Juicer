from juicer.utils import *
from scrapy.http import FormRequest

class LogIn(JuicerSpider):
    name = "login_pa"
    start_urls = ['https://www.patientslikeme.com']

    def parse(self,response):
        hdoc = HTML(response)
        auth = "".join(hdoc.select('//meta[@name="csrf-token"]/@content').extract())
        formdata={'utf8':'\xe2\x9c\x93','authenticity_token':str(auth),'userlogin[login]':'kiran_moka','userlogin[password]':'kiRan_29','commit':'Sign in','walgreens_continue_url':''}
        yield FormRequest('https://www.patientslikeme.com/login',self.parse_login,response,formdata=formdata)
		#,meta = {'dont_redirect': False,'handle_httpstatus_list': [302]})

    def parse_login(self,response):
        hdoc = HTML(response)
	    url = "".join(hdoc.select('//a[@href="/forums"]/@href').extract())
	    import pdb;pdb.set_trace()
        if 'http' not in url: url = 'https://www.patientslikeme.com'+url
	    url = 'https://www.patientslikeme.com/forum/plm/topics'
     	headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		    'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'en-US,en;q=0.8','Connection':'keep-alive',
		    'Host':'www.patientslikeme.com','If-None-Match':'W/"a09cc34620ab0d9239eacc4f792a3ee5"',
		    'Referer':'https://www.patientslikeme.com/whats_new/people','Upgrade-Insecure-Requests':'1',
		    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
			    }
        yield Request(url,self.parse_next,response,headers=headers)

    def parse_next(self,response):
        hdoc = HtmlXPathSelector(response)
    	import pdb;pdb.set_trace()
