from juicer.utils import *

class QuoraBoardSpider(JuicerSpider):
    name = 'quora_board'

    #http://www.quora.com/Matt-Schiavenza/boards
    #@url(["http://www.quora.com/.*/boards[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        board_urls = hdoc.select('//a[@class="light"]/@href')
        for board_url in board_urls:
            yield Request('http://www.quora.com' + textify(board_url), self.parse_boardlink, response)

    #http://www.quora.com/Neil-Russo/So-Long-Farewell/followers
    #@url(["http://www.quora.com/.*/.*/followers[^/]*$"])
    def parse_boardlink(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        board_members = hdoc.select('//a[@class="user"]/@href')
        for board_member in board_members:
            get_page('quora_terminal', 'http://www.quora.com' + textify(board_member))
