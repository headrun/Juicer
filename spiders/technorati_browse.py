from juicer.utils import *

def gen_start_urls(name):
    items = get_uncrawled_pages('technorati_browse',limit = 100)
    if not items:
        items = [{'url':'http://technorati.com/blogs/directory/overall/'}]

    for item in items:
        yield item['url']

class TechnoratiSpider(JuicerSpider):
    name = 'technorati_browse'
    allowed_domains = ['http://technorati.com/blogs/directory/overall/']
    start_urls =  gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = hashlib.md5(response.url).hexdigest()
        item.set('sk', sk) 
        item.set('got_page', True)
        item.set('url', response.url)
        
        yield item.process() 

        urls = [
            hdoc.select('//a[@class="next"]/@href')
        ]

        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(get_request_url(response), u) for u in urls]

        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.set('got_page', False)
            yield item.process()

        nodes = hdoc.select('//td[@class="site-details"]/h3/a/@href')
        for node in nodes:
            url = textify(node)
            item = Item(response, HTML)
            item.set('sk', url)
            item.set('url', urljoin(response.url, url))
            item.set('got_page', False)
            item.spider = 'technorati_terminal'
            
            yield item.process()


SPIDER = TechnoratiSpider()
 
