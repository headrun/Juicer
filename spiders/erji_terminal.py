from juicer.utils import *

class ErjiTerminalSpider(JuicerSpider):
    name = 'erji_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sub = xcode(textify(hdoc.select('//div[contains(@class, "t")]//th[@class="h"]/text()')))

        validateUri = "www.erji.net"

        forumUrl = "http://www.erji.net/"

        firstpostId = textify(hdoc.select('//form[@name="delatc"]//a[@name][1]/@name'))

        url = get_request_url(response)

        nodelist = hdoc.select('//div[@class="t t2"]')
        for node in nodelist:
            author = xcode(textify(node.select('.//tr[@class="tr1"]//th[@class="r_two"]//b/text()')))
            item.set('author', author)

            post = textify(node.select('.//div[@class="tiptop"]//a[contains(@href, "action=quote")]/@href')).split('&')[-2]
            postId = post.replace('pid=', '')
            threadId = textify(node.select('.//div[@class="tiptop"]//a[contains(@href, "action=quote")]/@href')).split('&')[2].split('tid=')[-1]
            discussionUri = "http://" + validateUri + "/" + threadId
            item.set('discussionUri', discussionUri)

            if "page=" in url:
                page = url.split('toread=')[1].split('page=')[1]
            else:
                page = 1

            link = "http://" + validateUri + "/read.php?tid=" + str(threadId) + "&fpage=0&toread=&page=" + str(page) + "#" + str(postId)
            item.set('link', link)

            discussionLink = "http://" + validateUri + "/read.php?tid=" + str(threadId) + "&fpage=0&toread=&page=" + str(page)
            item.set('discussionLink', discussionLink)

            authorUri = "http://www.erji.net/user/" + author
            item.set('authorUri', authorUri)

            authorLink = forumUrl + "search.php?authorid=" + author + "&digest=1"
            item.set('authorLink', authorLink)

            uri = discussionUri + "/" + postId
            item.set('uri', uri)

            if str(postId) == str(firstpostId):
                subject = sub
            else:
                subject = "RE:" + sub
            print "subject>>>>>>>>>>>>>>>", subject
            item.set('subject', subject)

            message_image = textify(node.select('.//th[@class="r_one"]//img/@src[contains(., "erji.net")]'))
            message_text = xcode(textify(node.select('.//th[@class="r_one"]//text()')))
            message = message_text + message_image
            item.set('message', message)

            tmptimestamp1 = textify(node.select('.//div[@class="tipad"]/text()[contains(., ": ")]')).split('Posted:')[-1].split("|")[0].split(' ')[1].split('-')
            timestamp1 = tmptimestamp1[2] + "-" + tmptimestamp1[1] + "-" + tmptimestamp1[0]
            timestamp2 = textify(node.select('.//div[@class="tipad"]/text()[contains(., ": ")]')).split('Posted:')[-1].split("|")[0].split(' ')[2] + ":00"
            timestamp = timestamp1 + " " + timestamp2
            item.set('timestamp', timestamp)

        last_page = textify(hdoc.select('//td[@align="left"]//div[@class="pages"]//a[last()]/@href')).split(' ')[0]
        last = int(last_page.split('page=')[-1]) + 1
        forum_id = last_page.split('tid=')[-1].split('&')[0]

        for page in range(1, last):
            next_page = "http://www.erji.net/read.php?tid=" + str(forum_id) + "&fpage=0&toread=&page=" + str(page)
            get_page(self.name, next_page)

        yield item.process()
