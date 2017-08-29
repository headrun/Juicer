from juicer.utils import *

class AlibabaTerminalSpider(JuicerSpider):
    name = 'alibaba_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk)

        title = textify(hdoc.select('//h2[@id="productTitle"]/text()'))
        item.set('title', title)

        product_information = {}
        nodelist = hdoc.select('//table[@id="productTbInfo"]//tr')
        for node in nodelist:
            key = textify(node.select('.//th[@class="proName"]')).replace(':', '')
            value = textify(node.select('.//td//text()'))
            product_information[key] = value
            product_information['FOB Price'] = product_information['FOB Price'].replace("Get Latest Price", "")
        item.set('product_information', product_information)

        quick_details = {}
        qnodelist = hdoc.select('//div[@id="detailProperty"]//table[@class="dbtable"]//td')
        for qnode in qnodelist:
            key = textify(qnode.select('.//span')).replace(':', '')
            value = textify(qnode.select('./text()')).strip()
            quick_details[key] = value
        item.set('quick_details', quick_details)

        image_url = textify(hdoc.select('//a[@id="productImg"]//img/@src'))
        item.set('image_url', image_url)

        packaging_delivery = {}
        packaging_delivery['delivery_details'] = textify(hdoc.select('//span[contains(text(), "Delivery Detail:")]//parent::td//following-sibling::td/text()'))
        packaging_delivery['packaging_details'] = textify(hdoc.select('//span[contains(text(), "Packaging Detail:")]//parent::td//following-sibling::td/text()'))
        item.set('packaging_delivery', packaging_delivery)

        specification = hdoc.select('//div[@class="dbcontent"]//p//text()')
        specification = [textify(s) for s in specification]
        item.set('specification', specification)

        company_name = textify(hdoc.select('//a[@id="companyName"]/text()'))
        item.set('company_name', company_name)

        company_link = textify(hdoc.select('//a[@id="companyName"]/@href'))
        item.set('company_link', company_link)

        company_location = textify(hdoc.select('//div[@id="comanyLocation"]//div/text()')).replace('[', '').replace(']', '').strip()
        company_location = company_location.replace('\n', '').replace('\t', '')
        item.set('company_location', company_location)

        company_main_products = textify(hdoc.select('//div[@class="main-products-text"]/text()')).split(',')
        item.set('company_main_products', company_main_products)

        yield item.process()
