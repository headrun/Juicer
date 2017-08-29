from juicer.utils import *

class IdenticaFollowingSpider(JuicerSpider):
    name = 'identica_following'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        followings = []
        following = hdoc.select('//img//parent::a[@class="url entry-title"]/@href')
        for flwng in following:
            flwng = textify(flwng)
            get_page('identica_terminal', flwng)

        next_following = textify(hdoc.select('//li[@class="nav_next"]//a/@href'))
        if next_following:
            get_page(self.name, next_following)
