from juicer.utils import *

class WretchBlogSpider(JuicerSpider):
    name = 'wretch_blog'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response)

        feed_url = get_request_url(response) + '&rss20=1'
        item.set('feed_url', feed_url)

        blogpost_urls = hdoc.select('//div[@class="posted"]//a/@href[contains(., "postComments")]')
        for blogpost_url in blogpost_urls:
            blogpost_url = 'http://www.wretch.cc' + textify(blogpost_url)
            blogpost_url = blogpost_url.split('#')[0]
            get_page('wretch_blogpost', blogpost_url)

        yield item.process()
