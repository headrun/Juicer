from juicer.utils import *

class Listofnewspapers(JuicerSpider):
    name = 'listofnewspapers'
    start_urls = ['http://www.listofnewspapers.com/en/asia/chinese-newspapers-in-china.html']

    def parse(self, response):
        hdoc = HTML(response)
        print "response>>>>", response.url
        #country = ''.join(re.findall(r'newspapers-in-(\w+).html', response.url)).strip()
        country = 'china'
        print "country>>>>", country
        news_urls = hdoc.select_urls(['//div[@class="divlistcountries1"]//ul/li/a/@href'] ,response)
        file_name = country + "_listofnewspapers"
        file_name = "/home/headrun/venu/rss/" + file_name

        out_file = file(file_name, 'ab+')
        for news_url in news_urls:
            if "listofnewspapers.com" in news_url:
                continue
            out_file.write('%s\n' % (news_url))

        out_file.close()
