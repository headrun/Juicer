from juicer.utils import *

class Wikisources(JuicerSpider):
    name = 'wiki_sources'

    start_urls =['http://en.wikipedia.org/wiki/Category:Newspapers_published_in_China'
                ]

    def parse(self, response):
        hdoc = HTML(response)

        news_urls = hdoc.select_urls(['//div[@class="mw-content-ltr"]//ul/li/a/@href'] ,response)

        for url in news_urls:
            yield Request(url, self.parse_terminal, response)


    def parse_terminal(self, response):
        hdoc = HTML(response)

        url = textify(hdoc.select('//td//a[@class="external free"]//@href'))
        if not url:
            url = textify(hdoc.select('//li//a[@class="external text"]//@href'))

        if url and not "wikipedia" in url and not "facebook.com" in url and not "twitter.com" in url:

            country = "china"
            file_name = country + "_wikipedia_sources"
            file_name = "/home/headrun/venu/rss/" + file_name

            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (url))
            out_file.close()

