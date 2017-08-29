from juicer.utils import *

class EbayBrowseSpider(JuicerSpider):
    name = 'ebay_browse'
    allowed_domains = ['ebay.com']
    start_urls = 'http://shop.ebay.com/allcategories/all-categories?_rdc=1'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="FontGradientLink5"]//a/@href', '//td[@class="botpg-next"]//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="ttl"]//a[@class="vip"]/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-1].split('?')[0]
            get_page('ebay_terminal', url)

class EbayTerminalSpider(JuicerSpider):
    name = 'ebay_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('?')[0]
        item.set('sk', sk) 
        item.textify('name', '//h1[@class="vi-it-itHd"]')
        item.textify('shortdescription', '//div[@class="d-pad"]//li')
        item.textify('title', '//h1[@class="vi-is1-titleH1"]')
        item.textify('price', '//th[contains(text(),"Price")]//following-sibling::td//span//span')
        item.textify('originalprice', '//b[contains(text(),"Original price")]//parent::span')
        item.textify('discountedprice', '//b[contains(text(),"Discounted price")]//parent::span')
        item.textify('currentbid', '//th[contains(text(),"Current bid")]//following-sibling::td//span//span')
        item.textify('startingbid', '//th[contains(text(),"Starting bid")]//following-sibling::td//span//span')
        item.textify('winningbid', '//th[contains(text(),"Winning bid")]//following-sibling::td//span//span')
        item.textify('bidhistory', '//span[@class="vi-is1-s6"]//span//a[@rel="nofollow"]//span')
        item.textify('shipping', '//span[@id="fshippingCost"]')
        item.textify('delivery', '//div[@class="sh-TblCnt"]//b[not(contains(string(),"opens"))]')
        item.textify('coverage', '//th[contains(text(),"Coverage")]//following-sibling::td//div')
        item.textify('returns', '//td[@class="vi-rpd-miyContent"]')
        item.textify('primarycategory', '//ul[@class="in"]//li[1]//a')
        item.textify('secondarycategory', '//ul[@class="in"]//li[2]//a')
        item.textify('tertiarycategory', '//ul[@class="in"]//li[3]//a')
        item.textify('sellerid', '//span[@class="mbg-nw"]')
        item.textify('sellerpositivefeedback', '//span[@class="s-gray z_a"]')
        item.textify('itemlocation', ('//td[contains(text(),"Item location")]//following-sibling::td','//th[contains(text(),"Item Location")]//following-sibling::td//span'))
        item.textify('shipsto', '//td[contains(text(),"Ships to")]//following-sibling::td')
        item.textify('sellsto', '//td[contains(text(),"Sells to")]//following-sibling::td')
        item.textify('image', '//td[@class="vs_w-a"]//img/@src')
        item.textify('history', '//td[contains(text(),"History")]//following-sibling::td//a')
        item.textify('payments', ('//div[@id="payDet1"]', '//th[contains(text(),"Payment")]//following-sibling::td//div/text()'))
        item.textify('itemnumber', '//td[contains(text(),"Item number:")]//following-sibling::td')
        item.textify('itemcondition', '//td[contains(text(),"Item condition")]//following-sibling::td')

        yield item.process()
        got_page(self.name, response)

