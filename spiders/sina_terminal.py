from juicer.utils import *

class SinaTerminalSpider(JuicerSpider):
    name = 'sina_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split(".html")[0].split("_")[1]
        item.set('sk', sk)

        author = xcode(textify(hdoc.select('//strong[@id="ownernick"]/text()')))
        item.set('author', author)

        authorUri = "user://blog.sina.com.cn/" + author
        item.set('authorUri', authorUri)

        authorLink = textify(hdoc.select('//div[@class="info_btn1"]//a/@href[contains(., "qing.weibo")]'))
        item.set('authorLink', authorLink)

        subject = xcode(textify(hdoc.select('//div[@class="articalTitle"]//h2')))
        item.set('subject', subject)

        uri = "blog://blog.sina.com.cn/" + sk
        item.set('uri', uri)

        link = get_request_url(response)
        item.set('link', link)

        message_text = xcode(textify(hdoc.select('//div[@id="sina_keyword_ad_area2"]//text()')))

        message_image = textify(hdoc.select('//div[@id="sina_keyword_ad_area2"]//p//img/@src')).replace(' ', ',')

        message = message_text + message_image
        item.set('message', message)

        tags = hdoc.select('//td[@class="blog_tag"]//h3//a')
        tags = [xcode(textify(tag)) for tag in tags]
        item.set('tags', tags)

        timestamp1 = textify(hdoc.select('//span[@class="time SG_txtc"]/text()')).replace(")", "").replace("(", "").split(" ")[0]
        timestamp1 = timestamp1.split('-')
        timestamp1 = timestamp1[2] + "-" + timestamp1[1] + "-" + timestamp1[0]

        timestamp2 = textify(hdoc.select('//span[@class="time SG_txtc"]/text()')).replace(")", "").replace("(", "").split(" ")[1]

        timestamp = timestamp1 + " " + timestamp2
        item.set('timestamp', timestamp)

        yield item.process()
