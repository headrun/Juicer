from juicer.utils import *

class QypeSpider(JuicerSpider):
    name = 'qype_browse'
    allowed_domains = ['qype.co.uk']
    start_urls = 'http://www.qype.co.uk/uki/all_categories'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="borough-tree-popup__column"]//div//a/@href',\
                                 '//strong[@class="next_page"]//a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//h3[@class="category-review__name"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('-')[0].split('place/')[-1]
            get_page('qype_terminal', url, sk=sk)
