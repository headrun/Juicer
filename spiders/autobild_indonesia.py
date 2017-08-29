from juicer.utils import *
from dateutil import parser

class AutobildIndonesia(JuicerSpider):
    name = "autobild_indonesia"
    start_urls = ['http://www.autobild.co.id/']

    def parse(self,response):
        hdoc = HTML(response)

        links = hdoc.select('//ul[@class="box"]//a/@href').extract()
        for link in links[:4]:
            yield Request(link,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        article_links = hdoc.select('//article[@class="item"]')

        for articlelink in article_links:
            link = textify(articlelink.select('.//p[@class="headline"]/a/@href'))

            if 'http://usedcar.autobild.co.id/read/2016/06/07/17393/32/12/Ada-67.889-Unit-Mitsubishi-Pajero-Sport-Tahun-2009-2014-Kena-Recall-Mitsubishi-Mengapa' in response.url:
                continue
            dt_added = textify(articlelink.select('.//p[@class="textheader"]/text()')).split(',')[-1].strip().split(' ')
            month = textify(dt_added[1])
            date_dict = {'January':'Januari','February':'Februari','March':'Maret','April':'April','May':'Mei','June':'Juni','July':'Juli','August':'Agustus','September':'September','October':'Oktober','November':'Nopember','December':'Desember'}
            for key,value in date_dict.iteritems():
                if value == month:
                    month = key
            dt_added = textify(dt_added[0]) + ' ' + month + ' ' + textify(dt_added[-1])
            dt_added = parse_date(xcode(dt_added))
            dt_added1 = get_timestamp((dt_added) - datetime.timedelta(hours=9))
            if dt_added1 < get_current_timestamp()-86400*30:
            #if dt_added < self.cutoff_dt:
                is_next = False
                continue
            yield Request(link,self.details,response,meta={'date_added':dt_added1})

        try:next_page = hdoc.select('//span[@class="prevnext"]/a[not(contains(text(),"Last"))]/@href').extract()[0]
        except: next_page = ''
        if next_page != '' and is_next:
            print next_page
            yield Request(next_page,self.parse_next,response)

    def details(self,response):
        hdoc = HTML(response)
        date_added = response.meta['date_added']
        title = textify(hdoc.select('//div[@class="detailisi"]//h3//text()'))
        author = textify(hdoc.select('//div[@class="detailisi"]/p[@class="textheader"]/text()')[-1]).strip('By :')
        text = textify(hdoc.select('//div[@class="textdetail"]/p//text()')) or textify(hdoc.select('//div[@class="textdetail"]/div//text()'))
        import pdb;pdb.set_trace()
        '''item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',date_added)
        item.set('author',{'name':xcode(author)})
        item.set('text',xcode(text))
        yield item.process()'''
