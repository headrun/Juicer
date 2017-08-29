from juicer.utils import *

class StumbleuponFollowerSpider(JuicerSpider):
    name = 'stumbleupon_follower'

    #http://www.stumbleupon.com/stumbler/skyblue101/connections/followers
    #@url(["http://www.stumbleupon.com/stumbler/.*/connections/followers", "http://www.stumbleupon.com/.*/connections/followers/[0-9].*"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        follower = hdoc.select('//a[@class="connection-link"]/@href')
        for flwr in follower:
            get_page('stumbleupon_terminal', 'http://www.stumbleupon.com' + textify(flwr))

        next_follower = textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_follower:
            print "next_follower>>>>>>>>.", next_follower
            get_page(self.name, 'http://www.stumbleupon.com' + textify(next_follower))
