from juicer.utils import *
import feedparser

def get_urls():
    urls = file('/home/headrun/venu/adobe_urls', 'r').readlines()
    _urls = []
    for url in urls:
        _urls.append(url.replace('\n',''))

    return _urls

class Adobe(JuicerSpider):
    name = 'adobe_urls'
    start_urls = get_urls()

    def parse(self, response):
        hdoc = HTML(response)

        rss_urls = hdoc.select_urls(['//link[@rel="alternate"]/@href'], response)
        rss_urls = [urlparse.urljoin(response.url, rss_url) for rss_url in rss_urls]

        for url in rss_urls:
            feeds = feedparser.parse(url)
            if len(feeds['entries'])>1:
                print url
