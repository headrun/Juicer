from juicer.utils import *

class StumbleuponFollowingSpider(JuicerSpider):
    name = 'stumbleupon_following'

    #http://www.stumbleupon.com/stumbler/skyblue101/connections/following
    #@url(["http://www.stumbleupon.com/stumbler/.*/connections/following", "http://www.stumbleupon.com/.*/connections/following/[0-9].*"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        following = hdoc.select('//a[@class="connection-link"]/@href')
        for flwng in following:
            get_page('stumbleupon_terminal', 'http://www.stumbleupon.com' + textify(flwng))

        next_following = textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_following:
            print "next_following>>>>>>>>.", next_following
            get_page(self.name, 'http://www.stumbleupon.com' + textify(next_following))
