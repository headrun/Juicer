from juicer.utils import *

class AllmenusTerminalSpider(JuicerSpider):
    name = 'allmenus_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        print "response:",response.url
        urls = hdoc.select_urls('//div[@class="location_mid_module alpha"]//ul/li/a/@href',response)
        print "urls:",urls
        for url in urls:
            get_page(self.name,url)
            url  = url
            yield Request(url, self.parsedetails, None)
    def parsedetails(self,response):    
        print "response5:",response.url
        hdoc = HTML(response) 
        item = Item(response, HTML)
        sk = get_request_url(response)
        ref_url = response.url
        item.set('sk',sk)
        item.textify('title','//div[@class="grid_6 alpha"]//h2')
        item.textify('address','//address[@class="border_top address_txt"]')
        item.textify('phone','//p[@id="restaurant_info_phone"]')
        yield item.process()
        got_page(self.name, response)
