from juicer.utils import *

class ReviewcentreSpider(JuicerSpider):
    name = 'reviewcentre_browse'
    allowed_domains = ['reviewcentre.com']
    start_urls = 'http://www.reviewcentre.com/site_map.php'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="content SiteMap"]//ul//li//ul//li//a/@href',\
                                 '//div[@class="Pagination"][1]//a[contains(text(),"Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="FirstSection"]//h2//a/@href', response)
        for url in terminal_urls:
            sk = url.split('reviews')[-1].split('.html')[0]
            get_page('reviewcentre_terminal', url, sk=sk)
