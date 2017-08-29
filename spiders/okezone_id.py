from juicer.utils import*
from dateutil import parser
import datetime
import time

class Okezone_ID(JuicerSpider):
    name = 'okezone_id'
    start_urls = ['http://www.okezone.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories =  hdoc.select('//div[@class="carousel-inner carousel-inner-break carousel-inner-navmenu"]/div[@id="tab1"]/div[@class="row"]/a/@href').extract()
        for cat in categories:
            if 'okezone.com/ligainggris/?utm_source=wp&utm_medium=box' in cat or 'pilkada.okezone.com/?utm_source=wp&utm_medium' in cat:
                continue
            yield Request(cat,self.parse_indexlink,response)

    def parse_indexlink(self,response):
        hdoc = HTML(response)
        index_link = hdoc.select('//a[@title="okezone celebrity index"]/@href').extract() 
        if not index_link:
            index_link = hdoc.select('//div[@class="navbar-inner"]//a[contains(text(), "Indeks")]/@href').extract()[0]
        yield Request(index_link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        now = datetime.datetime.now().date()
        for i in range(300):
            dates = str(datetime.datetime.strftime(now - datetime.timedelta(days=i), '%Y/%m/%d'))
            url = response.url + '/'+dates
            date_added = get_timestamp(parse_date(xcode(dates)) - datetime.timedelta(hours=9))
            if date_added > get_current_timestamp()-86400*30:
                yield Request(url, self.parse_main_links,response)

    def parse_main_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="news-content"]//h4/a/@href').extract() or hdoc.select('//div[@class="news-content"]//p/a/@href').extract() or hdoc.select('//ul[@class="list-berita"]//a[@title]/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)


        nxt_pg = textify(hdoc.select('//div[@class="pagination-komentar"]//a[contains(.,"%s")]/@href'%u'\xbb')) or textify(hdoc.select('//ul[@class="pagination"]//a[contains(.,"%s")]/@href'%u'>'))or textify(hdoc.select('//div[contains(@class, "pagination-komentar")]//a[contains(.,"%s")]/@href'%u'>'))
        
        if nxt_pg:
            yield Request(nxt_pg,self.parse_main_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[contains(@class, "title")]//h1//text()'))
        date = textify(hdoc.select('//div[@class="meta-post"]//time//text()')) or textify(hdoc.select('//p[@class="imgnews-datetime"]//text()')) or textify(hdoc.select('//div[contains(@class, "title")]//h1/following-sibling::span//text()'))

        date = ''.join(re.findall('\d+.*',date))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        text =  textify(hdoc.select('//div[@id="contentx"]//text()')) or textify(hdoc.select('//div[@class="bg-detail-rexo"]//p//text()')) or textify(hdoc.select('//div[@class="ctn-desc"]//p//text()'))       

        junk_txt = textify(hdoc.select('//div[@id="contentx"]//script//text()')) or textify(hdoc.select('//div[@id="contentx"]//a[@title]//text()'))
        text = text.replace(junk_txt,'')
        author = textify(hdoc.select('//div[@class="author "]//div[@class="nmreporter"]/div//text()')) or textify(hdoc.select('//p[@class="imgnews-jurnalist"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
#        yield item.process()
