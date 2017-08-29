from juicer.utils import *

class Flipkart_urls(JuicerSpider):
    name = 'flipkart_urls'
    start_urls = ['http://www.flipkart.com/brands']
    allowed_domains = ['www.flipkart.com']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select_urls('//div[contains(@class,"brand-row")]//a/@href')
        for url in urls:
            yield Request(url, self.parse_brand, response)

    def parse_brand(self, response):
        hdoc = HTML(response)

        product_urls = hdoc.select_urls('//div[contains(@id,"products")]//a/@href')
        for p_url in product_urls:
            p_url = urlparse.urljoin(response.url, p_url)
            p_url = p_url.replace('/p/', '/product-reviews/')
            p_id = ''.join(re.findall(r'pid=(\w+)&.*', p_url))
            _id = ''.join(re.findall(r'product-reviews/(\w+)\?pid', p_url))
            p_url = re.sub(r'&ref.*','', p_url.replace(_id, _id.upper()))
            if p_id:get_page('flipkart_terminals1', p_url, sk=p_id)

        next_page = textify(hdoc.select('//div[@id="pagination"]/a[contains(text(),"Next")]/@href'))
        if next_page:yield Request(next_page, self.parse_brand, response)

