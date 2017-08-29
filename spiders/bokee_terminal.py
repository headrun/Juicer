from juicer.utils import *

class BokeeTerminalSpider(JuicerSpider):
    name = 'bokee_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        link = get_request_url(response)
        item.set('link', link)

        if 'viewdiary' in link:
            sk = get_request_url(response).split('/viewdiary.')[1].split('.html')[0]
            item.set('sk', sk)

        else:
            sk = get_request_url(response).split('.shtml')[0].split('/')[-1]
            item.set('sk', sk)

        author = get_request_url(response).split('http://')[-1].split('.bokee.com')[0]
        item.set('author', author)

        authorUri = "user://www.bokee.com/" + author
        item.set('authorUri', authorUri)

        uri = "blog://www.bokee.com/" + sk
        item.set('uri', uri)

        authorLink = "http://" + author + ".bokee.com/"
        item.set('authorLink', authorLink)

        subject = xcode(textify(hdoc.select('//div[@class="entry-title"]//div//h2/text()')))
        item.set('subject', subject)

        time = textify(hdoc.select('//div[@class="fbzt"]//span[@class="f"]//span[@class="pub-time"]/text()'))
        time = time + ":00"
        date = textify(hdoc.select('//div[@class="fbzt"]//span[@class="f"]//span[@class="pub-date"]/text()')).split('.')
        date = date[2] + "-" + date[1] + "-" + date[0]

        timestamp = date + " " + time
        item.set('timestamp', timestamp)

        message = xcode(textify(hdoc.select('//div[@class="entry-body nerr"]//text()')))
        item.set('message', message)

        yield item.process()
