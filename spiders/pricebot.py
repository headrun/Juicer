import urllib
from urlparse import urlparse
from juicer.utils import *

class Hotelpricebot(JuicerSpider):
    name = "pricebot"
    start_urls = "http://www.hotelpricebot.com/usa.html"


    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="xboxcontent"]/a')
        for node in nodes:
            city_name = textify(node.select('./text()'))
            city_url = textify(node.select('.//@href'))
            yield Request(city_url, self.parse_listing, response, meta = {"city_name":city_name})


    def parse_listing(self, response):
        hdoc = HTML(response)
        lists = hdoc.select('//div[@class="hhead"]//div[@class="hhname"]')

        for li in lists:
            url = textify(li.select('.//h3//a/@href')).split(" ")
            url = url[0]
            hotel_id = re.findall(r'hid=(\d+)', url)
            city_name = response.meta['city_name']
            from_date = self.date_op(datetime.datetime.now()+ datetime.timedelta(days=5))
            for i in range(2):
                to_date = self.date_op(datetime.datetime.now() + datetime.timedelta(days=i+7))
                #page_url = "http://search.hotelpricebot.com/SearchedHotel.aspx?destination=city:"+city_name+"&hotelID="+hotel_id[0]+"&checkin="+from_date+"&checkout="+to_date+"&Rooms=1&adults_1=2&languageCode=EN&currencyCode=USD"
                url = urlparse.urljoin(response.url, url)
                yield Request(url, self.get_cookie, response, meta ={'from_date':from_date, 'to_date':to_date, "city_name":city_name, "url": url})


    def parse_semiterminal(self, response):
        hdoc = HTML(response)
        url = response.url
        cook = {}
        url = re.findall(r"/Hotel/(\w+).htm", url)
        name = url[0]
        if name:
            terminal_url = "http://search.hotelpricebot.com/SearchedHotelRates.aspx?languageCode=EN&currencyCode=USD&fileName="+name+"&destination=city:"+response.meta['city_name']+"&radius=20km&checkin="+response.meta['from_date']+"&checkout="+response.meta['to_date']+"&Rooms=1&adults_1=2"
            cook = response.meta['cookie']
            yield Request(terminal_url, self.parse_terminal, response, cookies = cook)


    def parse_terminal(self, response):
        hdoc = HTML(response)
        #print "responseURL>>>>", response.url
        import pdb;pdb.set_trace()
        nodes = hdoc.select('//table[@id="hc_htl_pm_rates_content"]//tr')
        if nodes:
            for node in nodes:
                room_type = textify(node.select('.//td[@class="hc_tbl_col1"]/a//text()'))
                website_name = textify(node.select('.//@data-providername'))
                price = textify(node.select('.//td[@class="hc_tbl_col2"]/a//text()[not(contains(string(),"$"))]'))
                print "room type>>><<", room_type
                print "website>><<", website_name
                print "price>><<", price
                print"from_date<<>>", response.meta['from_date']
                print "to_date>><<", response.meta['to_date']


    def date_op(self, dateobj):
        dateobj = dateobj.isoformat(' ')
        date = dateobj.split(" ")
        date = date[0]
        return date


    def get_cookie(self, response):
        hdoc = HTML(response)
        cookie = {}
        url = response.url
        url = re.findall(r"/Hotel/(\w+).htm", url)
        name = url[0]
        if name :
            terminal_url = "http://search.hotelpricebot.com/SearchedHotelRates.aspx?languageCode=EN&currencyCode=USD&fileName="+name+"&destination=city:"+response.meta['city_name']+"&radius=20km&checkin="+response.meta['from_date']+"&checkout="+response.meta['to_date']+"&Rooms=1&adults_1=2"
        data = response.headers
        words = ['brandId', 'ViewedHotels', 'Tests', 'userID', 'a_aid', 'VisitGuid', 'Analytics']
        for k, v in  data.iteritems():
            if k == 'Set-Cookie':
                for i in v:
                    if "brandId" in i :
                        brandId = re.findall(r'brandId=(\d+)',i)
                        cookie['brandId'] = brandId[0]

                    if "ViewedHotels" in i :
                        ViewedHotels = re.findall(r'ViewedHotels=(\d+)',i)
                        cookie['ViewedHotels'] = ViewedHotels[0]

                    if "Tests" in i :
                        Tests = re.findall(r'Tests=(\d+)',i)
                        cookie['Tests'] =  Tests[0]

                    if "userID" in i :
                        userID = re.findall(r'userID=(\d+)',i)
                        cookie['userID'] = userID[0]

                    if  "a_aid" in i :
                        a_aid = re.findall(r'a_aid=(\d+)',i)
                        cookie['a_aid'] = a_aid[0]

                    if  "VisitGuid" in i :
                        VisitGuid = re.findall(r'VisitGuid=(\d.*);',i)
                        cookie['VisitGuid'] = VisitGuid[0]

                    if  "Analytics" in i:
                        Analytics = re.findall(r'Analytics=(\w.*EN)',i)
                        cookie['Analytics'] = Analytics[0]


        cookie['countryCode'] = 'US'
        cookie['currencyCode'] = 'USD'
        cookie['languageCode'] = 'EN'
        #@okie['Analytics'] = "ReferrerID=&Keyword=&WebPageID=7&LandingID=hotel:1106427&LanguageCode=EN" 
        cookie['__utma'] = "180945445.983820209.1352369492.1352443823.1352465971.3"
        cookie['__utmz'] = "180945445.1352369492.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
        cookie['affiliateClickId'] = "380056964"
        cookie['Tests'] = "20121105%2c000035E4;"
        cookie['checkin'] = response.meta['to_date']
        cookie['checkout'] = response.meta['from_date']
        cookie['search'] = "destination=city:"+response.meta['city_name']

        print "Came here", response.meta['url']
        yield Request(terminal_url, self.parse_terminal, response, headers = data)
