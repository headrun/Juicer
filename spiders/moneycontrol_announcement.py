from juicer.utils import *
from juicer.utils import *
class MoneycontrolAnnouncement(JuicerSpider):
    name = "moneycontrol_announcement"
    urls = []
    for i in range(0,3):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        date = str(date.date())
        urls.append('http://www.moneycontrol.com/stocks/stock_market/announcements_date.php?ann_date=%s' %date)
    start_urls = urls

    def parse(self,response):
        hdoc= HTML(response)
        urls = hdoc.select('//div[@class="MT12 PB10 brdb"]')

        for each_url in urls:
            url = textify(each_url.select('./p/a/@href')[0])
            yield Request(url,self.parse_info,response)

        next_page = textify(hdoc.select('//div[@class="FL"]//div[@class="gray2_11"]//a[contains(text(),"Next")]/@href'))
        if next_page:
            yield Request(next_page,self.parse,response)

    def parse_info(self,response):
         hdoc = HTML(response)
         title = textify(hdoc.select('//div[@class="FL"]//p[@class="PT5"]//span[@class="bl_15"]//text()'))
         text =textify(hdoc.select('//div[@class="FL"]//p[@class="PT10 b_12"]//text()'))
         date = textify(hdoc.select('//div[@class="MT10"]/div[@class="FL"]/p[@class="gL_10"]/text()'))
         date = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))

         item = Item(response)
         item.set("title",title)
         item.set("text",text)
         item.set("dt_added",date)
         item.set("url", response.url)
         yield item.process()
