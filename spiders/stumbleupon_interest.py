from juicer.utils import *

class StumbleuponInterestSpider(JuicerSpider):
    name = 'stumbleupon_interest'

    #http://www.stumbleupon.com/stumbler/skyblue101/interests
    #@url(["http://www.stumbleupon.com/stumbler/.*/interests", "http://www.stumbleupon.com/stumbler/.*/interests/[0-9].*"])
    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        interest_urls = hdoc.select('//a[@class="connection-link"]/@href')
        for interest_url in interest_urls:
            yield Request('http://www.stumbleupon.com' + textify(interest_url) + '/followers', self.parse_interestlink, response)

        next_interest = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_interest:
            get_page(self.name, next_interest)

    #http://www.stumbleupon.com/interest/Alternative%20Energy/followers
    #@url(["http://www.stumbleupon.com/interest/.*/followers", "http://www.stumbleupon.com/interest/.*/followers/[0-9].*"])
    def parse_interestlink(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        interest_members = hdoc.select('//a[@class="connection-link"]/@href')
        for interest_member in interest_members:
            get_page('stumbleupon_terminal', 'http://www.stumbleupon.com' + textify(interest_member))

        next_intmem = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_intmem:
            yield Request(next_intmem, self.parse_interestlink, response)
