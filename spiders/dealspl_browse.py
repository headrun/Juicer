from juicer.utils import *

class DealsplBrowseSpider(JuicerSpider):
    name = 'dealspl_browse'
    allow_domain = ['dealspl.us']
    start_urls = ['http://dealspl.us/sitemap.php']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//li[@class="padt5"][contains(text(), "Deals")]//ul//li//a/@href', \
                                 '//div[@class="page_number"]//a[contains(text(),"Next")]/@href'],response)

        for url in urls:
            get_page(self.name, url)

        import pdb;pdb.set_trace()
        terminal_urls = hdoc.select_urls(['//div[@class="deal_img_span"]//a/@href'], response)
        for url in terminal_urls:
            get_page('dealspl_terminal', url)

