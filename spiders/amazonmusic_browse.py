from juicer.utils import *

class AmazonMusicSpider(JuicerSpider):
    name = 'amazonmusic_browse'
    allowed_domains = ['amazon.com']
    start_urls = 'http://www.amazon.com/Artist-Music-Specialty/b?ie=UTF8&node=721517011'
    limit_start_urls = 2000

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//h2[contains(text(),"Artist Directory")]//parent::div//div[@class="prodImage"]//a/@href',\
                                 '//p[@class="seeMore"]//a/@href',\
                                 '//span[@id="twAlbumCountBottom"]//a/@href',\
                                 #'//td[@style="vertical-align:top;"]//a/@href',\
                                 '//span[@class="pagnNext"]//a/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="faceoutTitle"]//a/@href', response)
        for url in terminal_urls:
            get_page('amazonmusic_terminal', url)
