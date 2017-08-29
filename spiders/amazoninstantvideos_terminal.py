from juicer.utils import *

class AmazonInstantVideosTerminalSpider(JuicerSpider):
    name = 'amazoninstantvideos_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/ref')[-2]
        sk = sk.split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//div[@id="prod-details"]//h1')
        item.textify('synopsis', '//div[@class="prod-synopsis"]')
        customer_reviews = textify(hdoc.select('//span[@class="crAvgStars"]//a[contains(text()," customer reviews")]/text()')).split('customer reviews')[0]
        item.set('customer_reviews', customer_reviews)
        video_details = {}
        nodelist = hdoc.select('//div[@class="prod-other"]//ul//li')
        for node in nodelist:
            key = textify(node.select('.//strong/text()')).replace(':', ' ')
            if key:
                value = textify(node.select('./text()'))
                video_details[key] = value
        item.set('video_details', video_details)
        item.textify('img_url', '//img[@id="prod-img"]/@src')
        product_details = {}
        nodelist1 = hdoc.select('//b[contains(text(),"Product Details")]//parent::div[@class="bucket"]//div[@class="content"]//div[@style]')
        for node in nodelist1:
            key1 = textify(node.select('.//span[@style][not(contains(text(),"Starring:"))][not(contains(text(),"Supporting actors:"))]\
                                       [not(contains(text(),"Directed by:"))][not(contains(text(),"Genre:"))]')).replace(':', ' ')
            if key1:
                value1 = textify(node.select('./text()'))
                product_details[key1] = value1
        item.set('product_deatails', product_details)
        theartical_release_info = {}
        nodelist2 = hdoc.select('//b[contains(text(),"Theatrical Release Information")]//parent::div[@class="bucket"]//div[@class="content"]//ul/li')
        for node in nodelist2:
            key2 = textify(node.select('./b/text()'))
            value2 = textify(node.select('./text()'))
            theartical_release_info[key2] = value2
        item.set('theartical_release_info', theartical_release_info)
        item.textify('online_viewing', '//td[@id="file_info_0"]//div[@style]')
        item.textify('pc_download', '//td[@id="file_info_1"]//div[@style]')
        item.textify('TiVo box', '//td[@id="file_info_2"]//div[@style]')
        item.textify('Portable device', '//td[@id="file_info_3"]//div[@style]')
        yield item.process()
        got_page(self.name, response)
