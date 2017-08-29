from juicer.utils import *

class Newspaperdrive(JuicerSpider):
    name = 'newspaperdrive'
    start_urls = ['http://www.newspaperdrive.com/china/']

    def parse(self, response):
        hdoc = HTML(response)

        next_page = ''
        print "response>>>>", response.url
        #country = ''.join(re.findall(r'newspaperdrive.com/(\w+)/', response.url)).strip()
        country = "china"
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//table//tr//td[@width="681"]//a/@href'] ,response)
        file_name = country + "_newspaperdrive"
        file_name = "/home/headrun/venu/rss/" + file_name

        out_file = file(file_name, 'ab+')
        for news_url in news_urls:
            news_url = news_url.split('url=')[-1].strip()
            if "www.newspaperdrive.com" in news_url:
                continue
            out_file.write('%s\n' % (news_url))

        out_file.close()

        next_page = hdoc.select('//a[contains(text(), "Next")]/@href')
        if next_page:
            yield Request(next_page, self.parse, response)
