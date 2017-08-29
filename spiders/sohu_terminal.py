from juicer.utils import *

class SohuTerminalSpider(JuicerSpider):
    name = 'sohu_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk', sk)
        details1 = textify(hdoc.select('//div[@class="revoBtns03"]')) or \
                   textify(hdoc.select('//div[@class="profile_content"]')) or \
                   textify(hdoc.select('//div[@class="noteContainer"]'))
        if details1:
            item.set('details1', details1)

        yield item.process()
