from juicer.utils import *

def gen_start_urls():
    items = get_uncrawled_pages('technorati_terminal', limit=100 )
    for item in items:
        yield item['url']

class TechnoratiTerminalSpider(JuicerSpider):
    name = 'technorati_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = hashlib.md5(get_request_url(response)).hexdigest()
        url = get_request_url(response)
        item.set('sk', url)
        item.set('url', url)
        item.update_mode = 'custom'

        latest_blog = textify(hdoc.select('//div[@class="inner"][contains(h2,"Recent blog post")]//a/@href'))
        item.set('latest_blog', latest_blog)

        item.set('got_page', True)
        yield item.process()

        recent_blog_time = textify(hdoc.select('//ol[@class="post-list"]//div[not(contains(text(), " in "))][not(contains(@style, "border"))]'))
        #item.set('recent_blog_time', parse_date(recent_blog_time))
        item.set('recent_blog_time', recent_blog_time)
