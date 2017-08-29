from juicer.utils import *

class LivejournalTerminalSpider(JuicerSpider):
    name = 'livejournal_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        req_url = get_request_url(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk)
        item.textify('name', '//th[contains(text(),"Name")]//following-sibling::td')
        item.textify('url', '//span[@class="ljuser with-alias-value ljuser-name_"]//a[2]/@href')
        item.textify('region', '//a[@class="region"]')
        item.textify('countryname', '//a[@class="country-name"]')
        item.textify('locality', ('//a[@class="locality"]','//th[contains(text(),"Location")]//following-sibling::td//span'))
        item.textify('watching', '//div[@id="watching_body"]//a/@href')
        item.textify('memberofwatching', '//div[@id="mofs_body"]//a/@href')
        item.textify('watchingfeeds', '//div[@id="watchingfeeds_body"]//a/@href')
        fsurls = [url for url in hdoc.select_urls('//div[@id="friends_body"]//a/@href')]
        item.set('fsurls', fsurls)
        for url in fsurls:
            get_page('livejournal_terminal', url)
        fofsurls = [url for url in hdoc.select_urls('//div[@id="fofs_body"]//a/@href')]
        item.set(' fofsurls',  fofsurls)
        for url in  fofsurls:
            get_page('livejournal_terminal', url)

        yield item.process()
        got_page(self.name, response)
