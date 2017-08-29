from juicer.utils import *
from datetime import datetime

class Spider(JuicerSpider):
    name = "clickon"

    urls_list = []
    urls = ['Aracaju','OfertaNacional','OfertaNacional/lastdeals','SaoPaulo','SaoPaulo/lastdeals','Bauru','BaixadaSantista','BeloHorizonte','BeloHorizonte/lastdeals','BalnearioCamboriu','Brasilia','Brasilia/lastdeals','BetimContagem','Campinas','Campinas/lastdeals','CampoGrande','Cuiaba','Curitiba','Curitiba/lastdeals','Florianopolis','Florianopolis/lastdeals','Fortaleza','Fortaleza/lastdeals','Goiania','Goiania/lastdeals','Guarulhos','Jundiai','Joinville','Joinville/lastdeals','JuizdeFora','Londrina','Londrina/lastdeals','Maceio','Maceio/lastdeals','MogidasCruzes','Maringa','Maringa/lastdeals','Niteroi','Niteroi/lastdeals','PPrudenteeRegiao','Piracicaba','PortoAlegre','PortoAlegre/lastdeals','PocosdeCaldasVarginha','Recife','Recife/lastdeals','RibeiraoPreto','RioClaro','RiodeJaneiro','RiodeJaneiro/lastdeals','SorocabaItu','SaoPauloExtra','SaoPauloExtra/lastdeals','SaoJosedoRioPreto','SaoPauloABCD','SaoPauloABCD/lastdeals','SaoLuis','SaoLuis/lastdeals','SaoPauloAlphaville','SaoPauloAlphaville/lastdeals','SaoPauloAlphaville/lastdeals','SeteLagoas','TrianguloMineiro','PocosdeCaldasVarginha','PocosdeCaldasVarginha','Vitoria','Vitoria/lastdeals','ValedoAco','ValedoParaiba','ValedosSinos']
    for url in urls:
        main_url = "http://www.clickon.com.br/clickon-client-http-deal/" + url
        urls_list.append(main_url)
    start_urls = urls_list
    def parse(self, response):

        item = Item(response, HTML)

        hdoc = HTML(response)



        if "lastdeals" not in response.url:
            title = textify(hdoc.select('//div[@id="section-offer"]//h2//a/@title')).encode('utf-8')
            deal_price = textify(hdoc.select('//div[@id="box-buy"]//h3//a/text()'))
            actual_price = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[not(contains(@class, "discount"))]//a/text()')[0])
            savings = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[not(contains(@class, "discount"))]//a/text()')[-1])
            discount = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[contains(@class, "discount")]//a/text()'))
            description = textify(hdoc.select('//div[@class="info"]//p/text()')).encode('utf-8')

            if len(description) == 0:
                description = textify(hdoc.select('//div[@class="post left"]//p/text()')).encode('utf-8')
            deal_provider = textify(hdoc.select('//dl[@class="info-map addressCorner"]//dt/text()')).encode('utf-8')

            if len(deal_provider) == 0:
                deal_provider = textify(hdoc.select('//div[@class="address left"]//h5/text()')).encode('utf-8')
            address = textify(hdoc.select('//dd//address/text()')).encode('utf-8')

            if len(address) == 0:
                address = textify(hdoc.select('//div[@class="address left"]//address/text()')).encode('utf-8')
            total_sold = textify(hdoc.select('//div[@id="box-qt"]//h5/text()')).split(' ')[0]

            #currency = "R$"

            if "OfertaNacional" in response.url:
                city = ""
            else:
                city = response.url.split('/')[-1]


            country = "Brazil"
            sk = textify(hdoc.select('//div[@id="section-offer"]//h2//a/@href')).split('deal/')[-1].encode('utf-8')
            date = datetime.now()
            date = date.strftime("%d-%m-%y")
            deal_type = "todays_deal"


            yield Request(hdoc.select('//div[contains(@id, "side-deal")]//h3//a/@href'),self.parse_details, response)

        elif "lastdeal" in response.url:

            nodes = hdoc.select('//div[@class="PdealContent"]')

            for node in nodes:

                title = textify(node.select('.//h2/text()')).encode('utf-8')
                total_sold = textify(node.select('.//h3//strong/text()'))
                actual_price = textify(node.select('.//li[@class="f-left de"]/text()')).split(':')[-1].strip()
                deal_price = textify(node.select('.//li[@class="f-right"]//strong/text()'))
                discount = textify(node.select('.//div[@class="PdealImgDet"]/text()')).split('l')[-1].split(':')[-1].strip()
                savings = textify(node.select('.//div[@class="PdealImgDet"]/text()')).split('l')[0].split(':')[-1].strip()

                if "R$" in deal_price:
                    currency = "R$"

                if "OfertaNacional" in response.url:
                    city = ""
                else:
                    city = response.url.split('deal/')[-1].split('/')[0]

                country = "Brazil"
                sk = title
                date = ""
                address = ""
                deal_provider = ""
                deal_type = "past_deals"
                description = ""

        item.set('title', title)
        item.set('description', description)
        item.set('deal_provider',deal_provider)
        item.set('actual_price', actual_price)
        item.set('discount',discount)
        item.set('savings', savings)
        item.set('deal_price',deal_price)
        item.set('date',date)
        #item.set('currency', currency)
        item.set('country', country)
        item.set('sk', sk)
        item.set('deal_type', deal_type)
        item.set('address', address)
        item.set('total_sold', total_sold)
        item.set('city', city)

        yield item.process()


    def parse_details(self, response):

        item = Item(response, HTML)

        hdoc = HTML(response)

        title = textify(hdoc.select('//div[@id="section-offer"]//h2//a/@title')).encode('utf-8')
        deal_price = textify(hdoc.select('//div[@id="box-buy"]//h3//a/text()'))
        actual_price = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[not(contains(@class, "discount"))]//a/text()')[0])
        savings = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[not(contains(@class, "discount"))]//a/text()')[-1])
        discount = textify(hdoc.select('//ul[@id="box-value"]//li//h5/following-sibling::p[contains(@class, "discount")]//a/text()'))
        description = textify(hdoc.select('//div[@class="info"]//p/text()')).encode('utf-8')

        if len(description) == 0:
            description = textify(hdoc.select('//div[@class="post left"]//p/text()')).encode('utf-8')
        deal_provider = textify(hdoc.select('//dl[@class="info-map addressCorner"]//dt/text()')).encode('utf-8')

        if len(deal_provider) == 0:
            deal_provider = textify(hdoc.select('//div[@class="address left"]//h5/text()')).encode('utf-8')
        address = textify(hdoc.select('//dd//address/text()')).encode('utf-8')

        if len(address) == 0:
            address = textify(hdoc.select('//div[@class="address left"]//address/text()')).encode('utf-8')
        total_sold = textify(hdoc.select('//div[@id="box-qt"]//h5/text()')).split(' ')[0]
        #currency = "R$"

        if "OfertaNacional" in response.url:
            city = ""
        else:
            city = response.url.split('/')[-1]

        country = "Brazil"
        sk = response.url.split('deal/')[-1]
        date = datetime.now()
        date = date.strftime("%d-%m-%y")
        deal_type = "todays_deal"


        item.set('title', title)
        item.set('description', description)
        item.set('deal_provider',deal_provider)
        item.set('actual_price', actual_price)
        item.set('discount',discount)
        item.set('savings', savings)
        item.set('deal_price',deal_price)
        item.set('date',date)
        #item.set('currency', currency)
        item.set('country', country)
        item.set('sk', sk)
        item.set('deal_type', deal_type)
        item.set('address', address)
        item.set('total_sold', total_sold)
        item.set('city', city)

        yield item.process()
