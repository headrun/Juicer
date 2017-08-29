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

class Toponsocial(JuicerSpider):
    name = "toponsocial"
    start_urls = ["http://www.toponsocial.com/facebook-pages/pk-pages/page-3.html"
                ]

    def parse(self, response):
        hdoc = HTML(response)

        #import pdb;pdb.set_trace()
        #country = ''.join(re.findall(r'/facebook-pages/(\w+)-pages/', response.url))
        #country = COUNTRIES.get(country)
        country = 'pakistan'
        file_name = "/home/headrun/venu/facebook_pages/toponsocial_fb_pages_of_" + country

        nodes = hdoc.select('//div[@class="letter-list-info"]//a[@class="thumb"]')
        out = file(file_name, "ab+")
        for node in nodes:
            _id = textify(node.select('./@href'))
            _id = ''.join(re.findall(r'(\d+)', _id))
            rss_url = "https://www.facebook.com/feeds/page.php?id=%s&format=rss20" %(_id)
            title = textify(node.select('./@title')).encode('utf8').decode('ascii', 'ignore')

            out.write("%s\t%s\n" %(title, rss_url))

        out.close()

        next_page = textify(hdoc.select('//a/b[contains(text(), "Next")]/parent::a/@href'))
        yield Request(next_page, self.parse, response)
