from juicer.utils import *

class Pub(JuicerSpider):
    name = 'yahoo_vietnam'
    start_urls = 'http://vn.answers.yahoo.com/dir/index;_ylt=AibXGoT6gUQ6UnPJPBOqYO0_KopQ;_ylv=3'

    def parse(self, response):
        hdoc = HTML(response)

        urls = hdoc.select_urls(['//div[@id="yan-categories"]/div[@class="bd"]/ul//li//a/@href'], response)
        for url in urls:
            u_id = ''.join(re.findall(r'sid=(\d+)', url))
            rss_url = 'http://vn.answers.yahoo.com/rss/catq?sid=' + u_id
            out_file = file('/home/headrun/venu/vietnam_yahoo_feeds1','ab+')
            out_file.write('%s\n'%rss_url)
            out_file.close()
            print 'url>>', rss_url
            yield Request(url, self.parse, response)

