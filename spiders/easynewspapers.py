from juicer.utils import *

class Easynewspapers(JuicerSpider):
    name = 'easynewspapers'
    start_urls = [
                    'http://easynewspapers.com/asia/china-republic-taiwan'
                    'http://easynewspapers.com/asia/china-peoples-republic'
                ]

    def parse(self, response):
        hdoc = HTML(response)

        print "response>>>>", response.url
        #country = ''.join(re.findall(r'enewsreference.com/newspaper/(\w+).htm', response.url)).strip()
        #country = response.url.split('/')[-1]
        country = "china"
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//table[@id="sortable"]//td[contains(@class,"type")]//a/@href'] ,response)
        file_name = country + "_" + self.name
        file_name = "/home/headrun/venu/rss/" + file_name

        out_file = file(file_name, 'ab+')
        for news_url in news_urls:
            if self.name in news_url:
                continue
            out_file.write('%s\n' % (news_url))

        out_file.close()

