
from juicer.utils import *
from dateutil import parser

class  CustomToday(JuicerSpider):
    name = "custom_today"
    start_urls = ['http://customstoday.com.pk/']

    def parse(self,response):
        hdoc = HTML(response)
        #urls = hdoc.select('//div[@class="content"]/section[contains(@class,"cat-box")][position()>1]/div[@class="cat-box-title"]/h2/a/@href')
        headers = {'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36','Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer' : 'http://customstoday.com.pk/'}
        cookie = {'incap_ses_224_258179': 'it8dKeTGET0xZ742K9AbA4UyplQAAAAAlWrfmJJTJyaHrVPV3HrThw==' , 'optimizelyEndUserId': 'oeu1420178163620r0.9943692088127136','__qca': 'P0-864167088-1420178168751','incap_ses_32_258179' : 'a5xUbsdqvhU/92QRZbFxAEQ2plQAAAAAMk1q8h17li9egJkSAXQYbw==','visid_incap_258179':'sbVQc7szTn+vg0IFg6L/yIUyplQAAAAAQUIPAAAAAACoeP5PQshYy0GjbLomr7lO','incap_ses_257_258179':'VhTydSUvqFMnvvuxVgyRAzI3plQAAAAAWpQBzj97QTnt9sHxyagByg==','optimizelySegments':'%7B%7D','optimizelyBuckets':'%7B%7D','__utma':'164032045.875539211.1420178169.1420178169.1420178169.1','__utmb':'164032045.21.10.1420178169','__utmc':'164032045','__utmz':'164032045.1420178169.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','_ga':'GA1.3.875539211.1420178169','_em_vt':'2b4bb4acd44355d618e1a16a287954a63352457634-5865230854a646a8','_em_v':'d60c9dfa469077153e28a94c6d6554a63352457646-3040324554a646a8','__zlcmid':'SbeKIpGp8boppt' }

        urls = ['http://customstoday.com.pk/category/islamabadcustoms/','http://customstoday.com.pk/category/karachicustoms/','http://customstoday.com.pk/category/marketsofpakistan/','http://customstoday.com.pk/category/international-markets-2/','http://customstoday.com.pk/category/lahorecustoms/','http://customstoday.com.pk/category/shipping/','http://customstoday.com.pk/category/national/','http://customstoday.com.pk/category/op-ed/','http://customstoday.com.pk/category/business-2/','http://customstoday.com.pk/category/world-business/','http://customstoday.com.pk/category/chambers-and-trade-associations/','http://customstoday.com.pk/category/science-technology/technology-science-technology/','http://customstoday.com.pk/category/international/china/','http://customstoday.com.pk/category/international/russia/','http://customstoday.com.pk/category/international/saudi-arabia/','http://customstoday.com.pk/category/international/iran/','http://customstoday.com.pk/category/international/uk/','http://customstoday.com.pk/category/international/us/','http://customstoday.com.pk/category/international/canada/','http://customstoday.com.pk/category/international/australia/','http://customstoday.com.pk/category/international/korea/','http://customstoday.com.pk/category/international/japan/']
        for url in urls:
            print url
            yield Request(url,self.parse_next,response,headers=headers, cookies =cookie)

    def parse_next(self,response):
        hdoc = HTML(response)
        #import pdb;pdb.set_trace()
        f = open('tempk','w')
        f.write(response.body)
        #print response.body
        articles = hdoc.select('//div[@class="post-listing"]/article[@class="item-list"]/h2/a/@href')
        print articles
        for article in articles:
            print article

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select(''))
        text = textify(hdoc.select(''))
        dt_added = textify(hdoc.select(''))
        author = textify(hdoc.select(''))
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''

