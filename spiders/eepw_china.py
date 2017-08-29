from juicer.utils import *
from dateutil import parser

class Eepw(JuicerSpider):
    name = "eepw_china"
    start_urls = ['http://www.eepw.com.cn/news/articlelist/type/3','http://www.eepw.com.cn/news/articlelist/type/5','http://www.eepw.com.cn/news/articlelist/type/39','http://www.eepw.com.cn/news/articlelist/type/21','http://www.eepw.com.cn/news/articlelist/type/6','http://www.eepw.com.cn/news/articlelist/type/2','http://www.eepw.com.cn/news/articlelist/type/4','http://www.eepw.com.cn/news/articlelist/type/7','http://www.eepw.com.cn/info/articlelist/special/embedded/type/3','http://www.eepw.com.cn/info/articlelist/special/embedded/sub/3','http://www.eepw.com.cn/info/articlelist/special/embedded/sub/2','http://www.eepw.com.cn/info/articlelist/special/embedded/sub/56','http://www.eepw.com.cn/info/articlelist/special/embedded/type/5','http://www.eepw.com.cn/info/articlelist/special/eda/type/5','http://www.eepw.com.cn/info/articlelist/special/eda/sub/60','http://www.eepw.com.cn/info/articlelist/special/eda/sub/58','http://www.eepw.com.cn/info/articlelist/special/eda/sub/79','http://www.eepw.com.cn/info/articlelist/special/eda/type/3','http://www.eepw.com.cn/info/articlelist/special/analog/type/2','http://www.eepw.com.cn/info/articlelist/special/analog/sub/7','http://www.eepw.com.cn/info/articlelist/special/analog/sub/17','http://www.eepw.com.cn/info/articlelist/special/analog/sub/19','http://www.eepw.com.cn/info/articlelist/special/analog/sub/20','http://www.eepw.com.cn/info/articlelist/special/analog/sub/65','http://www.eepw.com.cn/info/articlelist/special/power/type/3','http://www.eepw.com.cn/info/articlelist/special/power/type/2','http://www.eepw.com.cn/info/articlelist/special/power/sub/16','http://www.eepw.com.cn/info/articlelist/special/power/sub/18','http://www.eepw.com.cn/info/articlelist/special/power/sub/51','http://www.eepw.com.cn/info/articlelist/special/power/sub/83','http://www.eepw.com.cn/info/articlelist/special/led/type/3','http://www.eepw.com.cn/info/articlelist/special/led/type/2','http://www.eepw.com.cn/info/articlelist/special/led/type/5','http://www.eepw.com.cn/info/articlelist/special/led/sub/77','http://www.eepw.com.cn/info/articlelist/special/led/sub/84','http://www.eepw.com.cn/info/articlelist/special/tm/type/3','http://www.eepw.com.cn/info/articlelist/special/tm/type/3','http://www.eepw.com.cn/info/articlelist/special/tm/type/2','http://www.eepw.com.cn/info/articlelist/special/tm/sub/46','http://www.eepw.com.cn/info/articlelist/special/tm/sub/45','http://www.eepw.com.cn/info/articlelist/special/tm/sub/44','http://www.eepw.com.cn/info/articlelist/special/rf/type/3','http://www.eepw.com.cn/info/articlelist/special/rf/type/2','http://www.eepw.com.cn/info/articlelist/special/rf/type/5','http://www.eepw.com.cn/info/articlelist/special/rf/sub/85','http://www.eepw.com.cn/info/articlelist/special/rf/sub/86','http://www.eepw.com.cn/info/articlelist/special/rf/sub/87','http://www.eepw.com.cn/info/articlelist/special/rf/sub/88','http://www.eepw.com.cn/info/articlelist/special/rf/sub/89','http://www.eepw.com.cn/info/articlelist/special/rf/sub/90','http://www.eepw.com.cn/info/articlelist/special/auto/type/3','http://www.eepw.com.cn/info/articlelist/special/auto/type/2','http://www.eepw.com.cn/info/articlelist/special/auto/sub/22','http://www.eepw.com.cn/info/articlelist/special/auto/sub/24','http://www.eepw.com.cn/info/articlelist/special/auto/sub/25','http://www.eepw.com.cn/info/articlelist/special/auto/sub/27','http://www.eepw.com.cn/info/articlelist/special/control/type/3','http://www.eepw.com.cn/info/articlelist/special/control/type/2','http://www.eepw.com.cn/info/articlelist/special/control/type/5','http://www.eepw.com.cn/info/articlelist/special/control/sub/30','http://www.eepw.com.cn/info/articlelist/special/control/sub/32','http://www.eepw.com.cn/info/articlelist/special/control/sub/29','http://www.eepw.com.cn/info/articlelist/special/control/sub/14','http://www.eepw.com.cn/info/articlelist/special/portable/type/2','http://www.eepw.com.cn/info/articlelist/special/portable/type/3','http://www.eepw.com.cn/info/articlelist/special/portable/type/5','http://www.eepw.com.cn/info/articlelist/special/portable/sub/72','http://www.eepw.com.cn/info/articlelist/special/portable/sub/73','http://www.eepw.com.cn/info/articlelist/special/portable/sub/74','http://www.eepw.com.cn/info/articlelist/special/portable/sub/75','http://www.eepw.com.cn/info/articlelist/special/portable/sub/76','http://www.eepw.com.cn/info/articlelist/special/medical/type/3','http://www.eepw.com.cn/info/articlelist/special/medical/type/2','http://www.eepw.com.cn/info/articlelist/special/medical/sub/71','http://www.eepw.com.cn/info/articlelist/special/medical/sub/69','http://www.eepw.com.cn/info/articlelist/special/safety/type/3','http://www.eepw.com.cn/info/articlelist/special/safety/type/2','http://www.eepw.com.cn/info/articlelist/special/safety/type/5','http://www.eepw.com.cn/info/articlelist/special/safety/sub/91','http://www.eepw.com.cn/info/articlelist/special/safety/sub/92','http://www.eepw.com.cn/info/articlelist/special/safety/sub/93','http://www.eepw.com.cn/info/articlelist/special/safety/sub/94','http://www.eepw.com.cn/info/articlelist/special/wireless/type/3','http://www.eepw.com.cn/info/articlelist/special/wireless/type/2','http://www.eepw.com.cn/info/articlelist/special/wireless/sub/42','http://www.eepw.com.cn/info/articlelist/special/wireless/sub/37','http://www.eepw.com.cn/info/articlelist/special/wireless/sub/36']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="column650"]//div[@class="listBox"]//h2//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        sub_title = textify(hdoc.select('//div[@class="subhead"]//text()'))
        text = textify(hdoc.select('//div[@class="content"]//p//text()'))
        if sub_title:
            text = sub_title + " " + text
        dt_added = textify(hdoc.select('//div[@class="authorTimeSource"]//text()')[2])
        dt_added = dt_added.split(u'\uff1a')
        dt_added = dt_added[1]
        author = textify(hdoc.select('//div[@class="authorTimeSource"]//text()')[1])
        author = author.split(u'\uff1a')
        author = author[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

