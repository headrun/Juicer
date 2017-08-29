from juicer.utils import *

class AmazonappsTerminalSpider(JuicerSpider):
    name = 'amazonapps_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/ref')[-2].split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//span[@id="btAsinTitle"]')
        item.textify('price', '//b[@class="priceLarge"]')
        item.textify('image', '//td[@id="prodImageCell"]//img/@src')
        item.textify('author', '//div[@class="buying"]/h1[@class="parseasinTitle"]/following-sibling::span//a')
        item.textify('platform', '//span[@class="mas-platform-value"]')
        item.textify('rated', '//span[@class="mas-platform-value"]/a')
        item.textify('avrg_custmr_rvws', '//span[@class="tiny"]//span[@class="crAvgStars"]/a')
        item.textify('amazon_likes', '//span[@class="amazonLikeCount"]')
        item.textify('availabilty', '//div[@class="availGreen"]//span')
        item.textify('latest_updates', '//h2[contains(text(),"Latest Updates")]//parent::div[@class="bucket"]//div[@class="content"]//ul//li')
        item.textify('product_features', '//h2[contains(text(),"Product Features")]//parent::td[@class="bucket normal"]//div//ul//li')
        item.textify('productdescription', '//div[contains(text(),"Product Description")]//following-sibling::div[@class="content"]')
        item.textify('developerinfo', '//div[contains(text(),"Developer Info")]//following-sibling::div//div[@class="aplus"]')
        item.textify('applicationpermissions', '//div[@id="appPermissions"]//ul//li')
        item.textify('category', '//span[@class="zg_hrsr_ladder"]//b//a')
        item.textify('Download restrictions', '//b[contains(text(),"Download restrictions")]//following-sibling::div')
        nodelist = hdoc.select('//h2[contains(text(),"Technical Details")]//parent::td[@class="bucket"]//div[@class="content"]//ul/li')
        yield item.process()
