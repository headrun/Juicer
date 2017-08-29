from juicer.utils import*
from dateutil import parser

class Baobinhdinh_VN(JuicerSpider):
    name = 'baobinhdinh'
    start_urls = ['http://www.baobinhdinh.com.vn/','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=1&macmp=1', 'http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=1&macmp=2','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=1&macmp=3','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=1&macmp=4','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=5&macmp=5','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=6&macmp=6','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=6&macmp=7','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=6&macmp=8','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=6&macmp=10','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=12&macmp=12','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=12&macmp=13','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=12&macmp=14','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=15&macmp=15','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=15&macmp=16','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=15&macmp=17','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=18&macmp=18','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=18&macmp=19','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=18&macmp=20','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=22&macmp=22','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=23&macmp=23','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=24&macmp=24','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=25&macmp=25','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=27&macmp=27','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=27&macmp=28','http://www.baobinhdinh.com.vn/ViewCat.aspx?macm=27&macmp=31']

    def parse(self,response):
        hdoc =  HTML(response)
        main_link = textify(hdoc.select('//div//p//span/preceding-sibling::a[@target="_self"]/@href'))
        if 'http' not in main_link: main_link = 'http://www.baobinhdinh.com.vn/' + main_link
        yield Request(main_link,self.parse_otherlinks,response)
    
    def parse_otherlinks(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//p[@class="pTitle"]//text()'))
        text = textify(hdoc.select('//div[@id="divContent"]//p//text()')) or textify(hdoc.select('//div[@id="divContent"]//h4//text()'))

        ext_txt = textify(hdoc.select('//p[@class="pTitle"]//text()'))
        text = text.replace(ext_txt,'')
        dt = textify(hdoc.select('//div[@style="clear: both; height: 25px;"]/span[@class="floatLeft fontsize12 color10"]//text()'))
        date = ''.join(re.findall('\d+.*',dt))
        date = date.replace(');','')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
#        yield item.process()


        links = hdoc.select('//div[@class="itemtinbaikhac"]/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.baobinhdinh.com.vn/' + link
            yield Request(link,self.parse_otherlinks,response)




