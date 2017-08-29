from juicer.utils import *

class Eazyhomepage(JuicerSpider):
    name = 'eazyhomepage'

    start_urls = ['http://www.eazyhomepage.com/Indian_newspapers.html'
                ]

    def parse(self, response):
        hdoc = HTML(response)

        news_urls = hdoc.select_urls(['//table[@width="754"]//a/@href'] ,response)

        for url in news_urls:
            yield Request(url, self.parse_terminal, response)


    def parse_terminal(self, response):
        hdoc = HTML(response)

        urls = hdoc.select_urls(['//td[@width="86"]//a/@href'], response)

        for url in urls:

            if "www.eazyhomepage.com" in url:
                continue
            country = "india"
            file_name = country + "_eazyhomepage_sources"
            file_name = "/home/headrun/venu/rss/" + file_name

            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (url))
            out_file.close()

