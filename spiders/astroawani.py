from juicer.utils import*
from dateutil import parser

class Astroawani_MY(JuicerSpider):
    name = 'astroawani'
    start_urls = ['http://www.astroawani.com/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list=[301]

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[contains(@class, "dropdown")]//a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        links = hdoc.select('//div[@class="title"] | //div[@class="listing-text"]')
        for link in links:
            date = textify(link.select('.//following-sibling::p[@class="listing-date"]/text()')) or textify(link.select('.//following-sibling::div[@class="date"]/text()'))
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec'}
            for key, value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)

            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(link.select('./a/@href')) or textify(link.select('./@href'))
            if 'http' not in link: link = 'http://www.astroawani.com' + link
            if 'photos/album' in link or 'lapor-langsung' in link or 'videos' in link:
                continue
            yield Request(link,self.parse_details,meta={'dont_redirect':True})

        nxt_pg = hdoc.select('//li[@class="active"]/following-sibling::li/a/@href').extract()
        if nxt_pg:
            nxt_pg = nxt_pg[0]
            if 'http' not in nxt_pg: nxt_pg = 'http://www.astroawani.com' + nxt_pg
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,meta={'dont_redirect':True,'handle_httpstatus_list':[301]})


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="row detail-title"]/h1/text()')) or textify(hdoc.select('//div[@class="padding_lr30 detail-title"]/h1/text()'))
        text1 = textify(hdoc.select('//strong/text() | //div[@class="detail-body-content"]/text()')) or textify(hdoc.select('//p[@class="video-description"]/text()'))
        text2 = textify(hdoc.select('//div[@class="detail-body-content"]//preceding-sibling::em//text()')) 
        junk_txt = textify(hdoc.select('//strong/a[@target="_blank"]/@href'))
        text = text1.replace(text2,'').replace(junk_txt, '')
        date1 = textify(hdoc.select('//div[@class="row detail-tagline"]//h6/text()'))
        date = textify(hdoc.select('//h6[@style="line-height: 1.3"]//text()')) or textify(hdoc.select('//div[@style="float:left"]/text()')) or textify(re.findall('.*:',date1)).strip(':').strip(' |')
        if 'Januari' in date:
            date = date.replace('Januari','Jan')
        elif 'Februari' in date:
            date = date.replace('Februari','Feb')
        elif 'Mac' in date:
            date = date.replace('Mac','March')
        elif 'Mei' in date:
            date = date.replace('Mei',"May")
        elif 'Julai' in date:
            date = date.replace('Julai','July')
        elif 'Ogos' in date:
            date = date.replace('Ogos','Aug')
        elif 'Oktober' in date:
             date = date.replace('Oktober','Oct')
        elif 'Disember' in date:
            date = date.replace('Disember','Dec')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="col-xs-12 col-sm-8 byline"]//a/text()')) or textify(hdoc.select('//h6[@style="line-height: 1.3"]//strong//text()')).strip(',')
        auth_url = textify(hdoc.select('//h6[@style="line-height: 1.3"]//strong//a/@href')) or textify(hdoc.select('//div[@class="col-xs-12 col-sm-8 byline"]//a/@href'))


        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(auth_url))
        item.set('xtags',['news_sourcetype_manual','malaysia_country_manual'])
#        yield item.process()
