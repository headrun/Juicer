from juicer.utils import *

class OpenlibraryTerminalSpider(JuicerSpider):
    name = 'openlibrary_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="edition"]//strong')
        about_book = textify(hdoc.select('//h1[@class="edition"]/text()')).strip()
        item.set('about_book', about_book)
        item.textify('published_year', '//h4[@class="publisher"]//strong')
        published_by = textify(hdoc.select('//h4[@class="publisher"]//a')).split(' ')[0]
        item.set('published_by', published_by)
        published_language = textify(hdoc.select('//h4[@class="publisher"]//a')).split(' ')[-1]
        if published_language:
            item.set('published_language', published_language)
        nodelist = hdoc.select('//div[@class="section"]//tr')
        book_details = {}
        for node in nodelist:
            key = textify(node.select('.//h6[@class="title"]'))
            value = textify(node.select('.//span[@class="object"]//text()')).strip()
            book_details[key] = value
        item.set('book_details', book_details)
        item.textify('book_image', '//div[@class="SRPCover bookCover"]//a[@class="coverLook"]//img/@src')
        yield item.process()
