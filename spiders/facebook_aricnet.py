from juicer.utils import *
from scrapy.http import FormRequest

class FacebookAricent(JuicerSpider):
    name = "facebook_aricent"
    start_urls = ['https://www.facebook.com/login.php']

    def parse(self,response):
        hdoc = HTML(response)
        formdata={'email':'sravanthi0894@gmail.com','pass':'sravs@5'}
        headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "accept-encoding":"gzip, deflate, sdch","accept-language":"en-US,en;q=0.8","cache-control":"max-age=0",
                    "upgrade-insecure-requests":"1",
                    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"}
        cookies = {"a11y":"%7B%22sr%22%3A0%2C%22sr-ts%22%3A1458721819537%2C%22jk%22%3A0%2C%22jk-ts%22%3A1458721819537%2C%22kb%22%3A1%2C%22kb-ts%22%3A1458721819537%2C%22hcm%22%3A0%2C%22hcm-ts%22%3A1458721819537%7D","datr":"FhLyVrWK7xKhrI1YdbhfeXrI"}
        return [FormRequest.from_response(response, formname='login_form', formdata={'email': 'sravanthi0894@gmail.com', 'pass': 'sravs@5'}, callback=self.parse_login)]
        #yield FormRequest('https://www.facebook.com/',self.parse_login,headers=headers,formdata=formdata,cookies=cookies)

    def parse_login(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        url = 'https://www.facebook.com/search/122114214480174/likers?ref=about'
        yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        import pdb;pdb.set_trace()

