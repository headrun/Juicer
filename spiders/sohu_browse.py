from juicer.utils import *

class SohuClassName(JuicerSpider):
    name = 'sohu_browse'
    start_urls = 'http://blog.sohu.com/'

    def parse(self, response):
        hdoc = HTML(response)
        #got_page(self.name, response)

        #import pdb; pdb.set_trace()

        urls = hdoc.select_urls(['//a[@target="_blank"]/@href[contains(., "/blog.sohu.com/")]'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//a[@target="_blank"]/@href[contains(., ".blog.sohu.com/")]'], response)

        for url in terminal_urls: get_page('sohu_terminal', url)
