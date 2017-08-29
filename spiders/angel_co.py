import pytz
from pytz import timezone
import datetime
from juicer.utils import *
from dateutil import parser
import request
from scrapy.http import FormRequest

class Angel_co(JuicerSpider):
    name = 'angel_co'
   # start_urls = ['https://angel.co/jobs']
    handle_httpstatus_list = ['404']
    #start_urls = ['https://angel.co/jobs#find/f!%7B%22locations%22%3A%5B%221620-Boston%2C%20MA%22%5D%2C%22keywords%22%3A%22python%22%2C%22remote%22%3Atrue%7D']
    start_urls = ['https://angel.co/login']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [404]

    def parse(self, response):
        #url =  'https://angel.co/job_listings/browse_startups_table?startup_ids%5B%5D=715002&startup_ids%5B%5D=76733&startup_ids%5B%5D=4245190&startup_ids%5B%5D=2360969&startup_ids%5B%5D=951423&startup_ids%5B%5D=4306372&startup_ids%5B%5D=103032&startup_ids%5B%5D=390602&startup_ids%5B%5D=1002592&startup_ids%5B%5D=1598919&listing_ids%5B0%5D%5B%5D=77111&listing_ids%5B1%5D%5B%5D=227215&listing_ids%5B2%5D%5B%5D=248977&listing_ids%5B3%5D%5B%5D=255937&listing_ids%5B4%5D%5B%5D=237327&listing_ids%5B5%5D%5B%5D=253563&listing_ids%5B6%5D%5B%5D=102274&listing_ids%5B6%5D%5B%5D=79548&listing_ids%5B7%5D%5B%5D=118734&listing_ids%5B8%5D%5B%5D=251482&listing_ids%5B9%5D%5B%5D=253538&tab=find&page=1'
        url = 'https://angel.co/jobs#find/f!%7B%22locations%22%3A%5B%221620-Boston%2C%20MA%22%5D%2C%22keywords%22%3A%22python%22%2C%22remote%22%3Atrue%7D'
        #url = 'https://angel.co/job_listings/startup_ids'
        fmt = '%a %b %d %Y %H:%M:%S'
        d = datetime.datetime.now(pytz.timezone("GMT"))
        session = requests.Session()
        response_ = session.get('https://angel.co/jobs#find/f!%7B%22locations%22%3A%5B%221620-Boston%2C%20MA%22%5D%2C%22keywords%22%3A%22python%22%2C%22remote%22%3Atrue%7D')
        h1 = session.cookies.get_dict()
        cookies = {'Content-Length' : 83
                'Content-Type' : 'application/x-www-form-urlencoded',
                'Date' : d.strftime(fmt) + ' GMT',
                'Referer' : 'https://angel.co/login',
                'Upgrade-Insecure-Requests' : 1,
                'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
                'visitor_hash' : 'dce372c078da61de05fe653c79339545',
                'X-Content-Type-Options' : 'nosniff',
                'X-Frame-Options' : 'SAMEORIGIN',
        }

        form_data = {'user_email' : 'rajaqx@gmail.com', 'user_password' : 'angelcopw',\
                'login_only' : 'true'}

        yield FormRequest(url, formdata = form_data, callback=self.parse_next, method = 'POST', \
                 cookies = cookies)

    def parse_next(self, response):
        import pdb;pdb.set_trace()
        print "Am here!"

