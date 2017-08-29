from juicer.utils import*
from dateutil import parser
from scrapy.http import FormRequest

class Banmuang_TH(JuicerSpider):
    name = 'banmuang_th'
    start_urls = ['http://www.banmuang.co.th/home']

    def parse(self,response):
        hdoc = HTML(response)
        categories = set(hdoc.select('//div[@class="mainmenu"]//a[@target="_blank"]/@href').extract())
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nxt_pg = textify(hdoc.select('//span[@id="newsList"]'))


        headers = {'PHPSESSID':'c97cb696ujmh1r1he9309nl8n2','__atuvc':'18%7C13','_cbclose':'1','_cbclose23447':'1','_ctout23447':'1','_pk_id..398f':'3e76c180a1ffbd63.1490763271.4.1490850555.1490786250.','_pk_id.5.398f':'b5088c60ed9956c4.1490763397.1.1490763397.1490763397.','_pk_ses..398f':'*','_uid23447':'088350D6.5','verify':'test','verify':'test'}

        
        import pdb;pdb.set_trace()
