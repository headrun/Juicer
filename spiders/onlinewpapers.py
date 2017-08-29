from juicer.utils import *

class Onlinenewspapers(JuicerSpider):
    name = "onlinenewspapers"
    start_urls = ['http://www.onlinenewspapers.com/china.htm']

    def parse(self, response):
        hdoc = HTML(response)

        #country = response.url.split("/")[-1].replace(".htm", "")
        country = "china"

        cookies = {"__utma" : "215455433.1637156382.1401257160.1401257160.1401257160.1",
                    "__utmb" : "215455433.1.10.1401257160",
                    "__utmc" : "215455433",
                    "__utmz" :"215455433.1401257160.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided)",
                    "h2" : "o",
                    "he" : "llo"
                 }

        news_urls = hdoc.select_urls(['//h1[@class="txt"]/following-sibling::ul[1]//li/a/@href'], response)
        news_urls = ["http://lt.webwombat.com/" + url.split("/")[-1] for url in news_urls]

        for news_url in news_urls:
            yield Request(news_url, self.parse_terminal, response, cookies=cookies, meta={"country" : country})

    def parse_terminal(self, response):
        hdoc = HTML(response)

        country = response.meta['country']
        file_name = "/home/headrun/venu/rss/" + country + "_ol_sources"
        print response.url
        out_file = file(file_name, "ab+")
        out_file.write("%s\n" %(response.url))
        out_file.close()
