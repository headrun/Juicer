from juicer.utils import *

class Baike(JuicerSpider):
    name = 'baike_urls'
    start_urls = ['http://www.baike.com/sitemap/sitemap_index.xml']

    def parse(self, response):
        hdoc = HTML(response)

        cutoff_date = parse_date('2013-03-18')
        nodes = hdoc.select('//sitemapindex/sitemap')
        for node in nodes:
            post_dt = textify(node.select('./lastmod'))
            post_dt = parse_date(post_dt)
            if post_dt >= cutoff_date:
                url = textify(node.select('./loc/text()'))
                out_file = file('/home/headrun/venu/baike/baike_urls','ab+')
                out_file.write('%s\n' %(url))
                out_file.close()
