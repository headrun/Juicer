from juicer.utils import *
from dateutil import parser

class  Otosia(JuicerSpider):
    name = "otosia"
    start_urls = ['http://www.otosia.com/tips/','http://www.otosia.com/berita/','http://www.otosia.com/review/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [301]


    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[contains(@class,"article-index-box")]')
        for node in nodes:
            date = textify(node.select('.//span[@class="newsdetail-schedule"]//text()')).split(',')[-1]
            date_dict = {'Juni':'June','Mei':'May','Desember':'Dec','Februari':'Feb','Maret':'Mar','Agustus':'Aug','Januari':'Jan','Juli':'Jul','Oktober':'Oct'}

            for key,value in date_dict.iteritems():
                if key in date:
                    date = date.replace(key,value)
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            url = textify(node.select('.//h2/a/@href'))
            if 'http:' not in url: url = 'http://www.otosia.com'+str(url)
            yield Request(url,self.parse_details,response)
        add_links =  hdoc.select('//div[contains(@class, "iBoxTop")]//a/@href').extract()
        for link in add_links:
            if 'http' not in link: link = 'https://www.otosia.com' + link
            yield Request(link,self.parse_details,response)

        next_page = textify(hdoc.select('//div[@class="mphold-g posr"]/a[@class="mpnext"]/@href'))
        if next_page and is_next:
            if 'index' in response.url:
                url = response.url.split('index')[0]
                url = url+str(next_page)
            else:
                url = response.url+str(next_page)
            yield Request(url,self.parse,response)
        

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="mobart-detail"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="OtoDetailNews"]//text()')) or textify(hdoc.select('//div[@class="OtoDetailNews"]//p//text()'))
        date  = textify(hdoc.select('//span[@class="newsdetail-schedule"]/text()')).split(',')[-1].strip()
        date_dict = {'Juni':'June','Mei':'May','Desember':'Dec','Februari':'Feb','Maret':'Mar','Agustus':'Aug','Januari':'Jan','Juli':'Jul','Oktober':'Oct'}
        for key,value in date_dict.iteritems():
            if key in date:
                date = date.replace(key,value)

        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@style="border-bottom: solid 1px #ECECEC;"]//following-sibling::span[@class="newsdetail-schedule"]//text()'))
        author = author.replace('Editor :','').replace('editor','')
        junk_txt = textify(hdoc.select('//div[@class="relatedContentBox"]//text()'))
        text = text.replace(junk_txt,'')

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()

