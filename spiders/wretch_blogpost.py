from juicer.utils import *

class WretchBlogpostSpider(JuicerSpider):
    name = 'wretch_blogpost'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response)
        item.set('sk', sk)

        comments = []
        cnodelist = hdoc.select('//ul[@class="comments-user"]')
        for cnode in cnodelist:
            details = {}
            details['post_comment'] = textify(cnode.select('.//li[@class="comments-word"]//p[3]'))
            post_by = textify(cnode.select('.//li[@class="comments-post"]//a[@class="postuser"]'))
            details['post_by'] = post_by
            if post_by:
                post_by_links = 'http://www.wretch.cc' + textify(cnode.select('.//li[@class="comments-post"]//a[@class="postuser"]/@href'))
                post_by_links1 = post_by_links.replace('/blog/', '/user/')
                get_page('wretch_terminal', post_by_links1)
                details['post_by_links'] = post_by_links1
            details['post_date'] = parse_date(textify(cnode.select('.//li[@class="comments-post"]')).split('at')[-1].split('comment')[0])
            comments.append(details)
        item.set('comments', comments)

        next_url = textify(hdoc.select('//span[@class="next"]//a/@href'))
        if next_url:
            next_url = next_url.split(' ')
            next_url = next_url[0]
            next_url = 'http://www.wretch.cc' + next_url
            next_url = next_url.split('#')[0]
            get_page(self.name, next_url)

        yield item.process()
