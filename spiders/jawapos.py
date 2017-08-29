from juicer.utils import *
from dateutil import parser
import urlparse
import urllib
from lxml import etree

class Jawapos(JuicerSpider):
    name = 'jawapos'
    start_urls = ['http://www.jawapos.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[contains(@id,"navbar-collapse")]//li/a[contains(@href,"/rubrik/")]/@href').extract()
        for category in categories:
            yield Request(category,self.parse_functn,response)

    def parse_functn(self,response):
        hdoc = HTML(response)
        newslinks = hdoc.select('//div[@class="sec-info"]/parent::a/@href').extract()
        for newslink in newslinks:
            yield Request(newslink,self.parse_details,response)

        link = textify(hdoc.select('//script[contains(text(),"jawapos")]'))
        link = str(textify(re.findall('url:.*"',link)).strip('url:').strip(' "'))
        i = 1
        nxt_pg = (urlparse.urljoin(link,urlparse.urlparse(link).path)).replace('"+pg+"',str(i))
        yield Request(nxt_pg,self.parse_nxt,response)

    def parse_nxt(self,response):
        data = json.loads(response.body)
        data = data['list']
        for data in data:
            url = data['url']
            yield Request(url,self.parse_details,response)

        next_pg = int(response.url.split('/')[-1]) + 1
        if url:
            next_pg = '/'.join(response.url.split('/')[:-1]) + '/' + str(next_pg)
            yield Request(next_pg,self.parse_nxt,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="detailtitle"]/text()'))
        text = textify(hdoc.select('//div[contains(@class,"newsContent")]/p//text()')).replace(u'\u200e','').replace(u'\u201c','').replace(u'\u201d','')
        date = textify(hdoc.select('//div[@class="page-header"]/div/text()'))
        month = date.split(' ')[2]
        day = date.split(',')[0]
        dicti = {'Januari':'January','Februari':'February','Maret':'March','April':'April','Mei':'May','Juni':'June','Juli':'July','Agustus':'August','September':'September','Oktober':'October','Nopember':'November','Desember':'December'}
        days = {'Minggu':'Sunday','Senin':'Monday','Selasa':'Tuesday','Rabu':'Wednesday','Kamis':'Thursday','Jumat':'Friday','Sabtu':'Saturday'}

        for key,value in dicti.iteritems():
             if key == month:
                date = date.replace(key,value)
        for keys,values in days.iteritems():
            if keys == day:
                date = date.replace(keys,values)

        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
        text_list =[]
        nxt_pg = hdoc.select('//div[@class="main-title newsPagingActive"]/parent::a/following-sibling::a/@href').extract()
        if nxt_pg! = []:
            for nxt in nxt_pg:
                f = urllib.urlopen(nxt).read()
                res = etree.HTML(f)
                text1 = textify(res.xpath('//div[contains(@class,"newsContent")]/p//text()'))
                text_list.append(text1)

        text = text + ' '.join(text_list)


        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
