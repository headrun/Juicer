from juicer.utils import *

COUNTRIES = {"in" : "india",
             "id" : "indonesia",
             "sg" : "singapore",
             "my" : "malaysia",
             "ph" : "philippines",
             "cn" : "china",
             "th" : "thailand",
             "vn" : "vietnam"
    }

class Min4(JuicerSpider):
    name = '4imn'
    start_urls = ['http://www.4imn.com/cn/']

    def parse(self, response):
        hdoc = HTML(response)

        print "response>>>>", response.url
        ##country = ''.join(re.findall(r'enewsreference.com/newspaper/(\w+).htm', response.url)).strip()
        #country = response.url.split('/')[-2]
        #country = COUNTRIES.get(country)
        country = "china"
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//div[@class="maincontent"]//td[@class="i"]/a/@href'] ,response)

        for news_url in news_urls:
            yield Request(news_url, self.parse_terminal, response, meta={"country" : country})

    def parse_terminal(self, response):
        hdoc = HTML(response)

        country = response.meta['country']
        file_name = country + "_" + self.name
        file_name = "/home/headrun/venu/rss/" + file_name

        news_url = hdoc.select('//div[@class="maincontent"]/div[@class="section group"]//table//td/a[@target="_blank"]/@href')
        news_url = news_url[0] if len(news_url) > 1 else news_url
        news_url = textify(news_url)

        if self.name in news_url:
            return

        out_file = file(file_name, 'ab+')

        out_file.write('%s\n' % (news_url))

        out_file.close()

