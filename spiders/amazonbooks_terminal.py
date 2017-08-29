from juicer.utils import *

class AmazonBooksTerminalSpider(JuicerSpider):
    name = 'amazonbooks_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/ref')[-2]
        sk = sk.split('/')[-1]
        item.set('sk', sk)
        discount1 = textify(hdoc.select('//tr[@class="youSavePriceRow"]//td[@class="price"]//span')).strip()
        discount2 = discount1.split('(')[-1]
        discount = discount2.split(')')[0]
        item.set('discount', discount)
        item.textify('book_title', '//span[@id="btAsinTitle"]/text()')
        item.textify('book_price', '//span[@class="listprice"]')
        item.textify('discount_price', '//b[@class="priceLarge"]')
        saving_amount = discount1.split('\n')[0]
        item.set('saving_amount', saving_amount)
        author = hdoc.select('//div[@class="buying"]/h1[@class="parseasinTitle"]/following-sibling::span[1]//a[1]')
        author = [ textify(a) for a in author]
        if author:
            author = author[0]
            item.set('author', author)
        item.textify('availabilty', '//span[@class="availGreen"]')
        item.textify('amazon_likes', '//span[@class="amazonLikeCount"]')
        item.textify('editorial_review', '//div[@class="productDescriptionWrapper"]')
        item.textify('img_url', '//td[@id="prodImageCell"]//a//img/@src')
        average_customer_reviews = textify(hdoc.select('//span[@class="tiny"]//span[@class="crAvgStars"]//a[contains(text()," customer reviews")]')).split('customer reviews')[0]
        item.set('average_customer_reviews', average_customer_reviews)
        nodelist = hdoc.select('//h2[contains(text(),"Product Details")]//parent::td[@class="bucket"]//div[@class="content"]//ul/li')
        product_details = {}
        for node in nodelist:
            key = textify(node.select('./b[not(contains(text(),"Average Customer Review:"))]')).strip()
            key = key.replace(':', ' ')
            if key:
                value = textify(node.select('./text()')).strip()
                product_details[key] = value
        item.set('product_details', repr(product_details))
        category = textify(hdoc.select('//li[@id="SalesRank"]/text()')).split(' in ')[-1]
        category = category.split('(\n')[0]
        category = [category] if category else []
        if 'Books' in textify(category):
            category = hdoc.select('//span[@class="zg_hrsr_ladder"]//b//a/text()')
            category = [textify(c) for c in category]
        item.set('category', category)
        yield item.process()
        got_page(self.name, response)
