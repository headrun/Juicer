from juicer.utils import *

class Thepaperboy(JuicerSpider):
    name = 'thepaperboy'
    start_urls = ['http://www.thepaperboy.com/china/newspapers/country.cfm']

    def parse(self, response):
        hdoc = HTML(response)

        country = 'china'
        news_urls = hdoc.select_urls(['//table[@width="700"]//td[@align="left"]/a/@href'] ,response)

        for url in news_urls:
            yield Request(url, self.parse_news, response, meta={"country" : country})


    def parse_news(self, response):
        hdoc = HTML(response)

        print "terminal url>>>>", response.url
        news_url = textify(hdoc.select('//h1/a/@href'))
        country = response.meta["country"]
        file_name = country + "_paperboy_sources"

        if not 'newspaper.cfm' in news_url:
            print 'newss>>>', news_url
            out_file = file(file_name, 'ab+')
            out_file.write('%s\n' % (news_url))
            out_file.close()
