from juicer.utils import *

class WeblogsTerminalSpider(JuicerSpider):
    name = 'weblogs_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1].split('.html')[0]
        item.set('sk', sk)

        item.textify('title', '//div[@class="SL"]//h1')
        item.textify('description', '//div[@class="content-full"]//div//p')

        feed_link =  textify(hdoc.select('//div[@class="syn"]//li//a/@href'))
        feed_link = 'http://weblogs.com.ph' + feed_link
        item.set('feed_link', feed_link)

        image_url = textify(hdoc.select('//div[@class="syn"]//a/img/@src'))
        image_url = 'http://weblogs.com.ph' + image_url
        item.set('image_url', image_url)

        item.textify('blog_url', '//div[@class="content-full"]//tr//b[contains(text(), "Blog URL:")]//parent::td//following-sibling::td//a')

        blog_tags = hdoc.select('//div[@class="content-full"]//tr//b[contains(text(), "Blog Tags:")]//parent::td//following-sibling::td//a')
        blog_tags = [textify(t) for t in blog_tags]
        item.set('blog_tags', blog_tags)

        blog_tags_url = hdoc.select('//div[@class="content-full"]//tr//b[contains(text(), "Blog Tags:")]//parent::td//following-sibling::td//a/@href')
        blog_tags_url = ['http://weblogs.com.ph' + textify(b) for b in blog_tags_url]
        item.set('blog_tags_url', blog_tags_url)

        item.textify('location', '//div[@class="content-full"]//tr//b[contains(text(), "Location:")]//parent::td//following-sibling::td')

        recent_blogs = []
        nodelist = hdoc.select('//div[@class="post"]')
        for node in nodelist:
            details = {}
            details['post_title'] = xcode(textify(node.select('.//div[@class="p-head"]//h2//a')))
            post_url = textify(node.select('.//div[@class="p-head"]//h2//a/@href'))
            details['post_url'] = 'http://weblogs.com.ph' + post_url
            posted_on = textify(node.select('.//p[@class="p-date-cat"]')).split(' in:')[0].split('on ')[-1]
            details['posted_on'] = parse_date(posted_on)
            post_tags = node.select('.//p[@class="p-date-cat"]//a')
            details['post_tags'] = [textify(p) for p in post_tags]
            recent_blogs.append(details)
        item.set('recent_blogs', recent_blogs)

        yield item.process()
