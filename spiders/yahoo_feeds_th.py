from juicer.utils import *

class Pub(JuicerSpider):
    name = 'yahoo_thailand'
    start_urls = 'http://th.answers.yahoo.com/dir/index;_ylt=AibXGoT6gUQ6UnPJPBOqYO1vIopQ;_ylv=3'

    def parse(self, response):
        hdoc = HTML(response)

        urls = hdoc.select_urls(['//div[@id="yan-categories"]/div[@class="bd"]/ul//li//a/@href'], response)
        for url in urls:
            u_id = ''.join(re.findall(r'sid=(\d+)', url))
            rss_url = 'http://th.answers.yahoo.com/rss/catq?sid=' + u_id
            out_file = file('/home/headrun/venu/thailand_yahoo_feeds1','ab+')
            out_file.write('%s\n'%rss_url)
            out_file.close()
            yield Request(url, self.parse, response)

