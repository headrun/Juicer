from juicer.utils import *

class MovotoTerminalSpider(JuicerSpider):
    name = 'movoto_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('.htm')[0]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="floatLeft"]')
        item.textify('price', '//span[@id="dppListPrice"]')
        item.textify('bed_room', '//span[@id="spanBedroom"]')
        item.textify('bathroom', '//span[@id="spanBathroom"]')
        item.textify('lot_size', '//td[contains(text(),"Lot Size:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('type', '//td[contains(text()," Type:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('year_biult', '//td[contains(text()," Year Built:")]//parent::tr//td[@class="dppBasicInfoBoxright"]//span')
        item.textify('days_movoto', '//td[contains(text()," Days on Movoto:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('mls_id', '//td[contains(text(),"MLS#:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('status', '//td[contains(text(),"Status:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('views', '//td[contains(text(),"Views:")]//parent::tr//td[@class="dppBasicInfoBoxright"]')
        item.textify('img_url', '//div[@id="ctl_main_HouseImage"]//img/@src')
        item.textify('description', '//div[@id="listingMarks"]')
        nodelist = hdoc.select('//div[@id="divFeatureList"]//table[@cellspacing="1"]//tr')
        details = {}
        for node in nodelist:
            key = textify(node.select('.//td[@class="infoLabel"]'))
            value = textify(node.select('.//td[@class="infoValue"]'))
            details[key] = value
        item.set('details', details)
        yield item.process()
        #got_page(self.name, response)
