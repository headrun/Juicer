from juicer.utils import *

class BlogbusTerminalSpider(JuicerSpider):
    name = 'blogbus_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('.html')[0].split('/')[-1]
        item.set('sk', sk)

        author = xcode(textify(hdoc.select('//div[@class="info"]//a[contains(@href, "/home.")]/text()')))
        item.set('author', author)

        authorUri = "user://www.blogbus.com/" + author
        item.set('authorUri', authorUri)

        authorLink = "http://home.blogbus.com/profile/" + author
        item.set('authorLink', authorLink)

        subject = xcode(textify(hdoc.select('//div[@class="postHeader"]//h2/text()')))
        item.set('subject', subject)

        uri = "blog://www.blogbus.com/" + sk
        item.set('uri', uri)

        link = get_request_url(response)
        item.set('link', link)

        tags = hdoc.select('//div[@class="tag"]//a[contains(@href, "/tag/")]/text()')
        tags = [xcode(textify(t)) for t in tags]
        item.set('tags', tags)

        timestamp1 = textify(hdoc.select('//div[@class="postHeader"]//h5/text()')).split(" ")[0]
        timestamp1 = timestamp1.split('-')
        timestamp1 = timestamp1[2] + "-" + timestamp1[1] + "-" + timestamp1[0]
        timestamp2 = textify(hdoc.select('//div[@class="postHeader"]//h5/text()')).split(" ")[1]
        timestamp = timestamp1 + " " + timestamp2
        item.set('timestamp', timestamp)

        message_text = xcode(textify(hdoc.select('//div[@class="postBody"]//p/text()')))

        message_image = textify(hdoc.select('//div[@class="postBody"]//p//img/@src')).replace(" ", ", ")

        message = message_text + message_image
        item.set('message', message)

        yield item.process()
