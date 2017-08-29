from juicer.utils import *

class W3newspapers(JuicerSpider):
    name = 'w3newspapers'
    start_urls = ['http://www.w3newspapers.com/chinese/']

    def parse(self, response):
        hdoc = HTML(response)

        print "response>>>>", response.url
        #country = ''.join(re.findall(r'www.w3newspapers.com/(\w+)/', response.url)).strip()
        country = "china"
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//div[@id="centercontent_mag"]//ul[not(contains(@class, "w3_otp"))]//a/@href'] ,response)
        file_name = country + "_w3newspapers_tamil"
        file_name = "/home/headrun/venu/rss/" + file_name

        out_file = file(file_name, 'ab+')
        for news_url in news_urls:
            if "http://www.w3newspapers.com" in news_url:
                continue
            out_file.write('%s\n' % (news_url))

        out_file.close()
