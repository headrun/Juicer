from juicer.utils import *

class WefollowSpider:
    def get_more_urls(self, response, hdoc):
        urls = hdoc.select_urls(['//a[contains(@href, "/twitter/")]/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//a[not(contains(@href, "/twitter/"))]/@href'], response)
        for url in terminal_urls:
            sk = url.rsplit('/', 1)[-1]
            get_page('wefollow_terminal', url, sk=sk)

class WefollowBrowse(JuicerSpider, WefollowSpider):
    name = 'wefollow_browse'
    start_urls = 'http://wefollow.com/'
    allowed_domains = ['wefollow.com']

    def parse(self, response):
        hdoc = HTML(response)
        self.get_more_urls(response, hdoc)
        got_page(self.name, response)

class WefollowTerminal(JuicerSpider, WefollowSpider):
    name = 'wefollow_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        self.get_more_urls(response, hdoc)
        sk = response.url.rsplit('/', 1)[-1]

        item = Item(response, HTML)
        item.textify('name', '//div[@id="profile_wrapper"]//h1')
        item.textify('description', '//div[@id="profile_wrapper"]//h2')

        counters = {}
        counter_nodes = hdoc.select('//div[@id="profile_wrapper"]//dl[contains(@class, "counter")]')
        for node in counter_nodes:
            key = textify(node.select('.//dd'))
            value = textify(node.select('.//dt'))
            value = int(value.replace(',', ''))
            counters[key] = value

        item.set('counters', counters)

        tags = [textify(x) for x in hdoc.select('//div[@id="profile_wrapper"]//div[@class="tag_name"]//a')]
        item.set('tags', tags)

        yield item.set_many({'sk': sk}).process()
        got_page(self.name, response, sk=sk)
