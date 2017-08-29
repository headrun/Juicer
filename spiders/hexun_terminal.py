from juicer.utils import *

class HexunTerminalSpider(JuicerSpider):
    name = 'hexun_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        subject = xcode(textify(hdoc.select('//div[@class="arttitle"]//strong/text()')))

        validateUrl = "mancityfans.net"

        forumUrl = "http://bbs.hexun.com"

        url = get_request_url(response)

        nodelist = hdoc.select('//div[@class="artcont"]//div[@class="lymod"]')
        for node in nodelist:
            author = xcode(textify(node.select('.//span[@class="f06c0"]//a/text()')))
            item.set('author', author)

            authorUri = "http://bbs.hexun.com/user/" + author
            item.set('authorUri', authorUri)

            authorLink = textify(node.select('.//span[@class="f06c0"]//a/@href'))
            authorLink = forumUrl + authorLink
            item.set('authorLink', authorLink)

            item.set('subject', subject)

            root = "http://bbs.hexun.com/" + url.split('post_')[1].split('_')[1]

            uri = root + "/" + textify(node.select('.//a/@href[contains(., "/editreply")]')).split('replyId=')[1].split('&')[0]
            item.set('uri', uri)

            discussionUri = root
            item.set('discussionUri', discussionUri)

            discussionLink = url
            item.set('discussionLink', discussionLink)

            link = url + "#" + textify(node.select('.//a/@href[contains(., "/editreply")]')).split('replyId=')[1].split('&')[0]
            item.set('link', link)

            message_text = xcode(textify(node.select('.//div[@class="txtmain"]//text()')))
            message_image = xcode(textify(node.select('.//div[@class="txtmain"]//img/@src')))

            message = message_text + " " + message_image
            item.set('message', message)

            tmptimestamp1 = textify(node.select('.//dl[@class="hfrcont"]//dd//p/text()[contains(., ":")]')).split('[')[1].split(']')[0].split(' ')[0].split('-')

            timestamp1 = tmptimestamp1[2] + "-" + tmptimestamp1[1] + "-" + tmptimestamp1[0]

            timestamp2 = textify(node.select('.//dl[@class="hfrcont"]//dd//p/text()[contains(., ":")]')).split('[')[1].split(']')[0].split(' ')[1]

            timestamp = timestamp1 + " " + timestamp2
            item.set('timestamp', timestamp)

        next_page  = textify(hdoc.select('//div[@class="botpage"]//div[@class="pagenum"]//a[@class="next"]/@href'))
        if next_page:
            get_page(self.name, next_page)

        yield item.process()
