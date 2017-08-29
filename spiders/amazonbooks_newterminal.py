from juicer.utils import *

class AmazonBooksNewTerminalSpider(JuicerSpider):
    name = 'amazonbooks_newterminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/ref')[-2]
        sk = sk.split('/')[-1]
        item.set('sk', sk)
        discount1 = textify(hdoc.select('//tr[@class="youSavePriceRow"]//td[@class="price"]//span')).strip()
        discount2 = discount1.split('(')[-1]
        discount = discount2.split(')')[0]
        if discount:
            item.set('discount', discount)
        item.textify('title', '//span[@id="btAsinTitle"]/text()')
        item.textify('price', '//b[@class="priceLarge"]')
        saving_amount = discount1.split('\n')[0]
        if saving_amount:
            item.set('saving_amount', saving_amount)
        author = hdoc.select('//div[@class="buying"]/h1[@class="parseasinTitle"]/following-sibling::span[1]//a[1]') or hdoc.select('//span[@class="contributorNameTrigger"]//a')\
                or hdoc.select('//div[@class="buying"]//span//a[not(contains(@href, "/review/"))]')
        author = [ textify(a) for a in author]
        if author:
            author = author[0]
            item.set('author', author)
        item.textify('availabilty', '//span[@class="availGreen"]')
        item.textify('amazon_likes', '//span[@class="amazonLikeCount"]')
        description = textify(hdoc.select('//div[@id="outer_postBodyPS"]//div[@id="postBodyPS"]'))
        if description:
            item.set('description', description)
        editorial_review = textify(hdoc.select('//div[@class="productDescriptionWrapper"]'))
        if editorial_review:
            item.set('editorial_review', editorial_review)
        item.textify('image_url', '//td[@id="prodImageCell"]//a//img/@src')
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
        yield item.process()
