from juicer.utils import *

class TheCatholicDirectorySpider(JuicerSpider):
    name = 'thecatholicdirectory_browse'
    allowed_domains = ['thecatholicdirectory.com']
    start_urls = 'http://www.thecatholicdirectory.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a/@href[contains(., "directory.cfm?fuseaction=show_state&country=US&state=")]',\
                                 '//a/@href[contains(., "&absolutecity=")]'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//a/@href[contains(., "directory.cfm?fuseaction=display_site_info&siteid=")]', response)

        for url in terminal_urls:
            sk = url.split('=')[-1]
            get_page('thecatholicdirectory_terminal', url, sk=sk)
