from juicer.utils import *

class Abyznewslinks(JuicerSpider):
    name = 'abyznewslinks'

    start_urls = ['http://www.abyznewslinks.com/hongk.htm',
                    ]

    def parse(self, response):
        hdoc = HTML(response)
        #print "response>>>>", response.url
        #country = response.url.split("/")[-1].replace('.html','')
        #print "country>>>>", country
        country = 'Hong_Kong'
        news_urls = hdoc.select_urls(['//a/@href'] ,response)
        file_name = country + "_worldnewspapers_sources"
        file_name = "/home/headrun/venu/rss/" + file_name

        for news_url in news_urls:
            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (news_url))
            out_file.close()

