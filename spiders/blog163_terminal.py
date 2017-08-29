from juicer.utils import *

class Blog163TerminalSpider(JuicerSpider):
    name = 'blog163_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/static/')[1].split('/')[0]
        item.set('sk', sk)

        author = xcode(textify(hdoc.select('//h1//span[@class="ztag pre"]/text()')))
        item.set('author', author)

        authorUri = "user://blog.163.com/" + author
        item.set('authorUri', authorUri)

        authorLink = textify(hdoc.select('//a[@class="fc03 m2a"]/@href[contains(., ".blog.")]'))
        item.set('authorLink', authorLink)

        subject = xcode(textify(hdoc.select('//span[@class="tcnt"]/text()')))
        item.set('subject', subject)

        uri = "blog://blog.163.com/" + sk
        item.set('uri', uri)

        link = get_request_url(response)
        item.set('link', link)

        timestamp1 = textify(hdoc.select('//span[@class="blogsep"]/text()[contains(., ":")]')).split(" ")[0]
        timestamp1 = timestamp1.split('-')
        timestamp1 = timestamp1[2] + "-" + timestamp1[1] + "-" + timestamp1[0]
        timestamp2 = textify(hdoc.select('//span[@class="blogsep"]/text()[contains(., ":")]')).split(" ")[1]
        timestamp = timestamp1 + " " + timestamp2
        item.set('timestamp', timestamp)

        message_text = xcode(textify(hdoc.select('//div[contains(@class, "bct fc05 fc11 ")]//text()')))
        message_image = textify(hdoc.select('//div[contains(@class, "bct fc05 fc11 ")]//div//img/@src')).replace(" ", ", ")

        message = message_text + message_image
        item.set('message', message)

        yield item.process()
