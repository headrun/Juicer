from juicer.utils import *

class FengniaoTerminalSpider(JuicerSpider):
    name = 'fengniao_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sub = xcode(textify(hdoc.select('//td[@class="navbar"]//h1/text()')))

        validateUri = "bbs.fengniao.com"

        forumUrl = "http://bbs.fengniao.com/forum/"

        firstpostId = textify(hdoc.select('//div[@align="center"][1]//div[@class="page"]//div[contains(@id, "edit")]//div[contains(@id, "post_message_")]/@id'))

        url = get_request_url(response)

        nodelist = hdoc.select('//div[@align="center"]//div[@class="page"]//div[contains(@id,"edit")]')
        for node in nodelist:
            post = textify(node.select('.//div[contains(@id, "post_message_")]/@id'))
            postId = post.replace('post_message_', '')
            threadId = url.split(".html")[0].split("forum/")[1].split("_")[0]
            discussionUri = "http://" + validateUri + "/" + threadId
            item.set('discussionUri', discussionUri)
            if "_" in url:
                page = int(url.replace(".html", "").split("forum/")[1].split("_")[1])
            else:
                page = 1
            link = "http://" + validateUri + "/forum/showthread.php?t=" + str(threadId) + "&amp;page=" + str(page) + "#" + str(post)
            item.set('link', link)
            discussionLink = "http://" + validateUri + "/forum/showthread.php?t=" + str(threadId) + "&amp;page=" + str(page)
            item.set('discussionLink', discussionLink)
            author = xcode(textify(node.select('.//a[@class="bigusername"]/text()')))
            item.set('author', author)

            authorUri = "http://bbs.fengniao.com/user/" + author
            item.set('authorUri', authorUri)

            authorLink = textify(node.select('.//div[contains(@id, "postmenu_")]//a[contains(@class, "biguser")]/@href[contains(., "userid")]'))
            item.set('authorLink', authorLink)

            uri = discussionUri + "/" + postId
            item.set('uri', uri)

            if str(post) == str(firstpostId) and page==1:
                subject = sub
            else:
                subject = "RE:" + sub
            item.set('subject', subject)

            message_text = xcode(textify(node.select('.//td[contains(@id, "td_post_")]//div[contains(@id, "post_message_")]//text()')))

            message_image = textify(node.select('.//td[contains(@id, "td_post_")]//div[contains(@style, "padding")]//a//img/@src'))

            message = message_text + message_image
            item.set('message', message)

            time = textify(node.select('.//td[contains(@class, "alt")][not(contains(@id, "td_post_"))]//span[@class="time"]/text()')).split(", ")[-1]
            time = time + ":00"

            date1 = textify(node.select('.//td[contains(@class, "alt")][not(contains(@id, "td_post_"))]//span[@class="time"]/text()')).split(", ")[0]
            if not "-" in date1:
                date1 = datetime.datetime.now()
                date1 = date1.strftime("%Y-%m-%d")
            date1 = date1.split('-')
            date = date1[2] + "-" + date1[1] + "-" + date1[0]


            timestamp = date + " " + time
            item.set('timestamp', timestamp)

        next_page = textify(hdoc.select('//td[@class="alt1"]//a[@class="smallfont"][contains(text(), ">")]/@href')).split(' ')[0]
        next_page = "http://bbs.fengniao.com/forum/" + next_page
        if next_page:
            get_page(self.name, next_page)

        yield item.process()
