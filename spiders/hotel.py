from juicer.utils import *
import urllib2

class Hotel(JuicerSpider):
    name = "hotel"
    start_urls = "http://search.hotelpricebot.com/SearchedHotel.aspx?destination=city:Aberdeen_Maryland&hotelID=1116946&checkin=2012-11-14&checkout=2012-11-16&Rooms=1&adults_1=2&languageCode=EN&currencyCode=USD"

    def parse(self, response):
        hdoc =HTML(response)
        cookie = {}
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
                        #ookie['VisitGuid'] = VisitGuid[0]

                    if  "Analytics" in i:
                        Analytics = re.findall(r'Analytics=(\w.*EN)',i)
                        cookie['Analytics'] = Analytics[0]


        cookie['countryCode'] = 'US'
        cookie['currencyCode'] = 'USD'
        cookie['languageCode'] = 'EN'
        cookie['checkin'] = "2012-11-14" 
        cookie['checkout'] = 2012-11-16
        cookie['search'] = "destination=city:"+"Aberdeen_Maryland"

        url = "http://search.hotelpricebot.com/SearchedHotelRates.aspx?languageCode=EN&currencyCode=USD&fileName=Clarion_Hotel_Aberdeen&destination=city:Aberdeen_Maryland&radius=20km&checkin=2012-11-14&checkout=2012-11-16&Rooms=1&adults_1=2"
        print "url>><<<", url
        print cookie
        yield Request(url, self.parse_terminal, response, cookies = cookie)



    def parse_terminal(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//table[@id="hc_htl_pm_rates_content"]//tr')
        import pdb;pdb.set_trace()
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

