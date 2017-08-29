from juicer.utils import *

class QuoraFollowerSpider(JuicerSpider):
    name = 'quora_follower'

    #http://www.quora.com/Matt-Schiavenza/followers
    #@url(["http://www.quora.com/.*/followers[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        follower_urls = hdoc.select('//a[@class="user"]/@href')
        for follower_url in follower_urls:
            get_page('quora_terminal', 'http://www.quora.com' + textify(follower_url))
