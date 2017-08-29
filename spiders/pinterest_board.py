from juicer.utils import *

class PinterestBoardSpider(JuicerSpider):
    name = 'pinterest_board'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('.com/')[-1].split('/')[1]
        item.set('sk', sk)

        user_id = get_request_url(response).split('.com/')[-1].split('/')[1]
        item.set('user_id', user_id)

        terminal_urls = hdoc.select_urls(['//div[@class="pin"]//a[@class="PinImage ImgLink"]/@href'], response)
        for url in terminal_urls: get_page('pinterest_boardpins', url)

        if '?page=' in  response.url:
            page_number = (response.url).split('?page=')[-1]
            nxt = (response.url).split('?page=')[0]
            nxt2 = nxt + '?page='
            page_number = int(page_number) + 1

        else:
            nxt2 = response.url + '?page='
            page_number = 2

        if terminal_urls:
            next_page = nxt2 + '%s' %str(page_number)
            get_page(self.name, next_page)
