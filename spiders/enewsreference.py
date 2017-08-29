from juicer.utils import *

class Enewsreference(JuicerSpider):
    name = 'enewsreference'
    start_urls = ['http://www.enewsreference.com/newspaper/china.htm']

    def parse(self, response):
        hdoc = HTML(response)

        print "response>>>>", response.url
        #country = ''.join(re.findall(r'enewsreference.com/newspaper/(\w+).htm', response.url)).strip()
        country = "china"
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//td[@width="300"]//a/@href'] ,response)
        file_name = country + "_enewsreference"
        file_name = "/home/headrun/venu/rss/" + file_name

        out_file = file(file_name, 'ab+')
        for news_url in news_urls:
            if "enewsreference.com" in news_url:
                continue
            out_file.write('%s\n' % (news_url))

        out_file.close()

