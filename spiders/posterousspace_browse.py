from juicer.utils import *

#FIXME: get tags from website itself insteado of hardcoding

class PosterousSpaceBrowseSpider(JuicerSpider):
    name = 'posterousspace_browse'
    start_urls = ['http://www.examples.posterous.com/']

    def parse(self, response):
        got_page(self.name, response)

        hdoc = HTML(response)
        for url in hdoc.select_urls(['//div[@id="container"]/nav[@id="categories"]/ul/li/a[contains(@href,"http://examples.posterous")]/@href'],response):
            get_page(self.name, url)
        for url in hdoc.select_urls(['//header/h2/a/@href'], response):
            get_page(self.name, url)
        for url in hdoc.select_urls(['//div[@class="body"]//p//a[contains(text(),"Visit")]/@href'], response):
            url = textify(url).split('.')[0].split('/')[-1]
            #FIXME: this logic may fail sometimes because visit me can be any domain and not the real posterous username
            url = "http://posterous.com/people/subscribers/%s" % url
            get_page(self.name, url)
            yield Request(url, self.parsenext, None)
    def parsenext(self,response):   
        hdoc = HTML(response)
        if "http://posterous.comhttp" in response.url:
            hdoc.url  = hdoc.url.split('http://posterous.comhttp')[-1]
            hdoc.url  = "http%s" % hdoc.url
        for url in hdoc.select_urls(['//td[@class="name"]//a/@href'],response):
            url = url.replace("people", "users")
            get_page('posterousspace_terminal', url)
        for url in hdoc.select_urls(['//a[@class="next_page"]/@href'],response):
            url =  url
            yield Request(url,self.parsenext,None)
