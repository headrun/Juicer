from juicer.utils import *
from scrapy.http import FormRequest
#from angel_startup_ids import startup_ids

class Angel_co(JuicerSpider):
    name = 'angel_browse'
    handle_httpstatus_list = [404, 302]
    start_urls = ["https://angel.co/login"]
        
    def parse(self, response):
        hdoc = HTML(response)
        auth = ''.join(hdoc.select('//meta[@name="csrf-token"]/@content').extract())
        form_data = {'user_email' : 'rajaqx@gmail.com', 'user_password' : 'angelcopw',\
            'login_only' : 'true', 'authenticity_token':auth}
        yield FormRequest(response.url, formdata=form_data, callback=self.parse_next)

    def parse_next(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        headers = response.headers
        print headers
        cookies = {}
        key, value = response.request.headers['Cookie'].split('=')
        cookies[key] = value
        auth = ''.join(hdoc.select('//meta[@name="csrf-token"]/@content').extract())
        url = 'https://angel.co/job_listings/startup_ids'
        form_data = {'tab' : 'find', 'filter_data[locations][]' : '1620-Boston,+MA',\
                'filter_data[remote]' : 'true', 'filter_data[keywords][]' : 'python',\
                'X-CSRF-Token' : auth}
        yield FormRequest(url, formdata=form_data,\
                    callback = self.parse_ids, cookies = cookies)

    def parse_ids(self, response):
        import pdb;pdb.set_trace()
