from juicer.utils import *

class XitekTerminalSpider(JuicerSpider):
    name = 'xitek_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sub = xcode(textify(hdoc.select('//td[@align="left"]//div[@class="ts"]//font[@color]/text()')))

        validateUri = "forum.xitek.com"

        forumUrl = "http://forum.xitek.com/"

        firstpostId = textify(hdoc.select('//table[@id][@summary][1]/@id'))

        url = get_request_url(response)

        nodelist = hdoc.select('//table[@id][@summary]')
        for node in nodelist:
            post = textify(node.select('./@id'))
            postId = post.split('pid')[-1]
            threadId = url.split('.html')[0].split('/thread-')[1].split('-')[0]

            discussionUri = "http://" + validateUri + "/" + threadId
            item.set('discussionUri', discussionUri)

            if "-1-1.html" in url:
                page = url.split('.html')[0].split('/thread-')[1].split('-')[1]
            else:
                page = 1

            pages = url.split('/thread-')[1].split('-')
            pageId = pages[1] + "-" + pages[2] + "-" + pages[3]

            link = "http://" + validateUri + "/thread-" + threadId + "-" + pageId + "#" + post
            item.set('link', link)

            discussionLink = "http://" + validateUri + "/thread-" + threadId + "-" + pageId
            item.set('discussionLink', discussionLink)

            author = xcode(textify(node.select('.//td[@class="pls"]//a//text()')))
            item.set('author', author)

            authorUri = "http://forum.xitek.com/user/" + author
            item.set('authorUri', authorUri)

            uri = discussionUri + "/" + postId
            item.set('uri', uri)

            if str(postId) == str(firstpostId) and page==1:
                subject = sub
            else:
                subject = "RE:" + sub
            item.set('subject', subject)

            message_text = xcode(textify(node.select('.//td[@class="t_f"][contains(@id, "postmessage")]//text()')))

            message_image = xcode(textify(node.select('.//td[@class="t_f"][contains(@id, "postmessage")]//img/@src')).replace(' ', ', '))

            message = message_text + ";" + message_image
            item.set('message', message)

            tmptimestamp = textify(node.select('.//td[@align="left"][@class="pls"]/text()[contains(., ":")]')).replace('\r\n', '').split(' ')

            timestamp1 = tmptimestamp[0].split('-')
            timestamp2 = timestamp1[2] + "-" + timestamp1[1] + "-" + timestamp1[0]
            timestamp3 = tmptimestamp[1] + ":00"

            timestamp = timestamp2 + " " + timestamp3
            item.set('timestamp', timestamp)

        next_page = textify(hdoc.select('//td[@class="plc"]//div[@class="pg"]//a[@class="nxt"]/@href'))
        if next_page:
            get_page(self.name, next_page)

        yield item.process()
