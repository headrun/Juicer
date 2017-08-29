from juicer.utils import *

class AmazonMusicTerminalSpider(JuicerSpider):
    name = 'amazonmusic_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/ref')[-2]
        sk = sk.split('/')[-1]
        item.set('sk', sk)
        item.textify('album_title', '//span[@id="btAsinTitle"] ')
        item.textify('artist', '//div[@class="buying"]//span[1]/a/text()')
        average_customer_review = textify(hdoc.select('//span[@class="tiny"]//span[@class="crAvgStars"]//a[contains(text(),"customer reviews")]')).split('customer reviews')[0]
        item.set('average_customer_review', average_customer_review)
        item.textify('price', '//b[@class="priceLarge"]')
        item.textify('amazon_likes', '//span[@class="amazonLikeCount"]')
        item.textify('availability', '//span[@class="availGreen"]')
        item.textify('editorial_reviews', '//div[@class="productDescriptionWrapper"]')
        nodelist = hdoc.select('//h2[contains(text(),"Product Details")]//parent::td[@class="bucket"]//div[@class="content"]//ul/li')
        product_details = {}
        for node in nodelist:
            key = textify(node.select('./b[not(contains(text(),"Average Customer Review:"))]')).replace(':', ' ')
            if key:
                value = textify(node.select('./text()'))
                product_details[key] = value
        item.set('product_details', product_details)
        item.textify('category', '//span[@class="zg_hrsr_ladder"]//b/a/text()')
        item.textify('image_url', '//td[@id="prodImageCell"]//img/@src')
        yield item.process()
        got_page(self.name, response)
