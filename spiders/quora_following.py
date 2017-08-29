from juicer.utils import *

class QuoraFollowingSpider(JuicerSpider):
    name = 'quora_following'

    #http://www.quora.com/Matt-Schiavenza/following
    #@url(["http://www.quora.com/.*/following[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        following_urls = hdoc.select('//a[@class="user"]/@href')
        for following_url in following_urls:
            get_page('quora_terminal', 'http://www.quora.com' + textify(following_url))
