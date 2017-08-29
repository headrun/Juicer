from juicer.utils import *
import scrapy

class LoginSpider(JuicerSpider):
    name = 'form_request'
    #start_urls = ['https://www.netflix.com/Login?locale=en-US']
    start_urls = ['https://www.netflix.com/Login?locale=en-DE']

    def parse(self, response):
        return scrapy.http.FormRequest.from_response(
            response,
            formdata={'username': 'fryan@veveo.net', 'password': 'veveo123'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        hdoc = HTML(response)
        if "authentication failed" in response.body:
            print "failed"

            return
