from juicer.utils import*
from dateutil import parser

class Doisongphapluat_VN(JuicerSpider):
    name = 'doisongphapluat_vn'
    start_urls = ['http://www.doisongphapluat.com/tin-tuc/', 'http://www.doisongphapluat.com/phap-luat/', 'http://www.doisongphapluat.com/su-kien-luat-su/', 'http://www.doisongphapluat.com/to-quoc-xanh/','http://www.doisongphapluat.com/kinh-doanh/','http://www.doisongphapluat.com/doi-song/', 'http://www.doisongphapluat.com/giai-tri/','http://www.doisongphapluat.com/the-thao/','http://www.doisongphapluat.com/cong-nghe/','http://www.doisongphapluat.com/giao-duc/','http://www.doisongphapluat.com/oto-xemay/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="info pkg"]')
        for node in nodes:
            date = textify(node.select('.//p[span[@class="time-ico"]]//text()'))
            date = ''.join(re.findall('\d{2}/\d{2}/\d{4}', date))
            date_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a/@href'))
            if  'http://trangphuclinh.vn/' in link:
                continue
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@class="current"]/following-sibling::a[1]/@href'))
        if nxt_pg  and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="art-title"]//text()')) or textify(hdoc.select('//div[@class="name-photo-slide"]//text()'))
        text = textify(hdoc.select('//div[@id="main-detail"]//p//text()')) or textify(hdoc.select('//div[@class="descript-photo"]//p//text()'))
        date = textify(hdoc.select('//p[@class="fl-right dt"]//text()')) 
        date = ','.join(re.findall('\d{2}/\d{2}/\d{4}|\d{2}:\d{2}',date))
        if not date:
            date = textify(hdoc.select('//label[@class="time-photo"]//text()'))
        dt_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
        author = textify(hdoc.select('//div[@class="name"]/a//text()'))
        author_link = textify(hdoc.select('//div[@class="name"]//p//a/@href'))
        if 'http' not in author_link: author_link = 'http://www.doisongphapluat.com' + author_link

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_link',xcode(author_link))
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
        yield item.process()
