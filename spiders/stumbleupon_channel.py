from juicer.utils import *

class StumbleuponChannelSpider(JuicerSpider):
    name = 'stumbleupon_channel'

    #http://www.stumbleupon.com/stumbler/gmc/channels/all
    #@url(["http://www.stumbleupon.com/stumbler/.*/channels/all", "http://www.stumbleupon.com/stumbler/.*/channels/all/[0-9].*"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        channel_urls = hdoc.select('//a[@class="connection-link"]/@href')
        for channel_url in channel_urls:
            yield Request('http://www.stumbleupon.com' + textify(channel_url) + '/followers', self.parse_channellink, response)

        next_channel = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_channel:
            get_page(self.name, next_channel)

    #http://www.stumbleupon.com/channel/PaulKedrosky/followers
    #@url(["http://www.stumbleupon.com/channel/.*/followers", "http://www.stumbleupon.com/channel/.*/followers/[0-9].*"])
    def parse_channellink(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        channel_members = hdoc.select('//a[@class="connection-link"]/@href')
        for channel_member in channel_members:
            get_page('stumbleupon_terminal', 'http://www.stumbleupon.com' + textify(channel_member))

        next_chnlmem = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[contains(text(), "next")]/@href'))
        if next_chnlmem:
            yield Request(next_chnlmem, self.parse_channellink, response)
