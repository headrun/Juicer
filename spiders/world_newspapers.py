from juicer.utils import *

class wordlnewspapers(JuicerSpider):
    name = 'world_newspapers'
    start_urls = [
                    'http://www.world-newspapers.com/china.html',
                    ]

    def parse(self, response):
        hdoc = HTML(response)

        print "response>>>>", response.url
        #country = response.url.split("/")[-1].replace('.html','')
        country = 'china'
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//td[@width="420"]//a[@target="_blank"]/@href'] ,response)
        file_name = country + "_worldnewspapers_sources"
        file_name = "/home/headrun/venu/rss/" + file_name

        for news_url in news_urls:
            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (news_url))
            out_file.close()

