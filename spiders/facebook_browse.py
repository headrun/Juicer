from juicer.utils import *

class FacebookSpider(JuicerSpider):
    name = 'facebook_browse'
    allowed_domains = ['facebook.com']
    start_urls = 'https://www.facebook.com/directory/pages/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="alphabet_list clearfix"]//a/@href',\
                                 '//div[@class="fbDirectoryBox mtm"]//li[@class="fbDirectoryBoxColumnItem uiListItem  uiListVerticalItemBorder"]//a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="uiInlineBlock uiInlineBlockMiddle"]//strong//a/@href'], response)

        for url in terminal_urls: get_page('facebook_terminal', url)
