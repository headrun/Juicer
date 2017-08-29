from juicer.utils import *
import urllib

class First_test(JuicerSpider):
    name = "redirecting"
    start_urls = ['https://www.facebook.com/']

    def parse(self, response):

        #url = 'http://www.filmweb.no/film/article1001802.ece'
        url = 'http://www.filmweb.no/template/art/filmomtale/related/review_related_render.jsp'

        hdrs = {"Accept" : "*/*",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-US,en;q=0.5",
"Content-Length":  "224",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Host":    "www.filmweb.no",
"Referer": "http://www.filmweb.no/film/article1001802.ece",
"User-Agent":  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:32.0) Gecko/20100101 Firefox/32.0",
"X-Requested-With" :  " XMLHttpRequest"
        }

        cookies = {"nPsegs=":"",
                    "ioo":"0000541483a4b65e0000",
                    "__utma":"84570382.2047965454.1410630594.1410632415.1410634597.3",
                    "__utmz":"=84570382.1410634597.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=http%3A%2F%2Fwww.filmweb.no%2Ffilm%2Farticle1001802.ece",
}

        data = {"id":"ART20131437",
            "id":  "CIN20140627",
            "id": "SFN20131348",
            "id":  "TDF20140195",
            "id":  "ACT20140609",
            "id":  "BVI20140175",
            "id":  "NOR20140372",
            "id":  "SFN20140088",
            "id":  "TDF20140616",
            "id":  "SBX20140592",
            "id":  "FOX20140203",
            "id":  "FOX20130594",
            "id":  "UIP20120568",
            "id":  "UIP20131275",
            "id":  "TDF20140410"
                            }
        payload = urllib.urlencode(data)
        yield Request(url, self.parse_terminal, response, method='POST', body=payload, headers=hdrs)

    def parse_terminal(self, response):

        hdoc = HTML(response)
        urls = hdoc.select('//a[@class="movie"]/@href')
        print urls


    def parse_terminal1(self, response):
        hdoc = HTML(response)

        print "in term>>>>", response.url
