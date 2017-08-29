from juicer.utils import *

class IdenticaFollowerSpider(JuicerSpider):
    name = 'identica_follower'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        followers = []
        follower = hdoc.select('//img//parent::a[@class="url entry-title"]/@href')
        for flwr in follower:
            flwr = textify(flwr)
            print "flwr>>>>>>>>>", flwr
            get_page('identice_terminal', flwr)

        next_follower = textify(hdoc.select('//li[@class="nav_next"]//a/@href'))
        if next_follower:
            print "next_follower>>>>>>>>.", next_follower
            get_page(self.name, next_follower)
