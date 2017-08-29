from juicer.utils import *

class AmazonInstantVideosSpider(JuicerSpider):
    name = 'amazoninstantvideos_browse'
    allowed_domains = ['amazon.com']
    start_urls = 'http://www.amazon.com/gp/search/other/ref=sr_sa_p_lbr_actors_browse-?rh=n%3A2625373011%2Cn%3A%212644981011%2Cn%3A%212644982011%2Cn%3A2858778011&bbn=2858778011&sort=-releasedate&pickerToList=lbr_actors_browse-bin&ie=UTF8&qid=1317968167'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//span[@class="refinementLink"]//parent::a/@href',\
                                 '//span[@class="pagnNext"]//a/@href'], response)
        #urls = hdoc.select_urls([re.findall('href="(/gp/search/ref=sr_in.*?)">', args.raw_data.data),\
         #                        '//span[@class="pagnNext"]//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="title"]//a/@href', response)
        for url in terminal_urls:
            get_page('amazoninstantvideos_terminal', url)
