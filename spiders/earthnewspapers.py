from juicer.utils import *

class Earthnewspapers(JuicerSpider):
    name = 'earthnewspapers'

    start_urls = ['http://www.earthnewspapers.com/China-Newspapers/index.html'
                ]

    def parse(self, response):
        hdoc = HTML(response)

        urls = hdoc.select_urls(['//a/@href'] ,response)
        print "news_urls>>>", len(urls)

        for url in urls:

            if "www.earthnewspapers.com" in url:
                continue

            if not url.startswith("http"):
                continue
            country = "china"
            file_name = country + "_earthnews_sources"
            file_name = "/home/headrun/venu/rss/" + file_name

            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (url))
            out_file.close()

