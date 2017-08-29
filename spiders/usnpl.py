from juicer.utils import *
import urlparse

class Usnpl(JuicerSpider):
    name = "usnpl"

    start_urls = ['http://www.usnpl.com/']

    def parse(self, response):
        hdoc = HTML(response)

        states = hdoc.select_urls(['//div[@id="data_box"]//a[contains(@href,"usnpl.com")]/@href'], response)

        for state in states:
            yield Request(state, self.parse_state, response)

    def parse_state(self, response):
        hdoc = HTML(response)

        links = hdoc.select_urls(['//div[@id="data_box"]/b/following-sibling::a[1]/@href'], response)
        for link in links:
            netloc = urlparse.urlparse(link)
            netloc = netloc.netloc
            out_file = file('/home/headrun/venu/usa_links', 'ab+')
            out_file.write('%s\n' % (netloc))
            out_file.close()
