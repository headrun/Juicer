from juicer.utils import *

class DealsandyouTerminalSpider(JuicerSpider):
    name = 'dealsandyou_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).replace('-d-n-y.html', '')
        sk = sk.split('-')[-1]
        sk = sk.replace('.html', '')
        item.set('sk', sk)
        title = textify(hdoc.select('//div[@class="name1"]'))
        if title:
            item.set('title', title)
            item.textify('description','//div[@class="the-deal-txt slidingD"]/p')
            image_url = hdoc.select('//div[@id="slider"]/ul/li/img/@src') or hdoc.select('//div[@class="dtailspic"]//img/@src')
            image_url = [textify(i) for i in image_url]
            item.set('image_url', image_url)
            reviews = xcode(textify(hdoc.select('//div[@class="slidingD"]/p'))).replace('\xe2\x80\x93', '')
            item.set('reviews', reviews)
            item.textify('buy','//div[@class="buy2pricenew"]', lambda k: k.replace('Rs ', ''))
            item.textify('highlights','//div[@class="boxnew1-vd-rightbox"]/div[@class="tablist1 slidingD"]/p/span/strong')
            item.textify('location','//div[@class="boxnew1-vd-rightbox"]/div[@class="slidingD"]/div')
            actual_price = textify(hdoc.select('//div[@class="rupees-value-box-txt-strike"]')).strip()
            item.set('actual_price', actual_price.replace('Rs ', ''))
            item.textify('price', '//div[@class="buy2pricenew"]', lambda x: x.replace('Rs ', ''))
            item.textify('discount', '//div[@class="rupees-value-box-txt"]', lambda z: z.split(' ')[-1].replace('%', ''))
            highlights = hdoc.select('//div[@class="tablist1 slidingD"]//ul//li') or hdoc.select('//div[@class="tablist1 slidingD"]//p')
            highlights = [textify(h) for h in highlights]
            item.set('highlights', highlights)
            item.textify('price_site', '//div[@class="buy2pricenew"]', lambda p: p.replace('Rs ', ''))
            item.textify('pay_balance', '//div[@class="buy3new"]//span', lambda y: y.replace('Rs ', ''))
            yield item.process()
        else:
            urls = hdoc.select_urls(['//div[@class="productui"]//div[@class="productuiblock"]/@onclick'], response)
            urls = textify(urls).split("location.href='")[-1].split("'")[0]
            yield Request(urls, self.parse, response)
