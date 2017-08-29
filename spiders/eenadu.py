from juicer.utils import*
from dateutil import parser

class EenaduNews(JuicerSpider):
    name = "eenadu_news"
    start_urls = ['http://www.eenadu.net/']

    def parse(self,response):
        hdoc = HTML(response)
        news_urls = hdoc.select('//li[contains(@class, "two-col-left-by-two")]//@href').extract()
        extra_urls = hdoc.select('//div[@id="submenu"]//ul/a/@href').extract()
        news_urls.extend(extra_urls)
        for url in news_urls:
            yield Request(url, self.parse, response)
        extra_url = hdoc.select('//div[@id="tajavarthalumore"]/a/@href')
        if extra_url:
            yield Request(extra_url, self.parse,response)
        national_urls=hdoc.select('//div[@class="col-left"]//a/@href').extract()
        news_urls = hdoc.select('//li[@class="two-col-left-by-two"]//a/@href').extract()
        national_urls.extend(news_urls)
        for url in national_urls:
            if 'video-gallery' in url or '/gallery.eenadu' in url:
                continue
            yield Request(url, self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//center//font[@size="+3"]//text()')) or textify(hdoc.select('//span[@style="font-family: EenaduU;"]/span[@style="color: #ff0000;"]/text()'))
        text = textify(hdoc.select('//font[@size="+2"]//text()')) or textify(hdoc.select('//p[@style="text-align: center;"]//following::p//text()'))
        dt = textify(hdoc.select('//span[@id="lblDateTime" ]//text()'))
        dat = dt.partition(',')[2]

        if u' \u0c2e\u0c47' in dat or u'\u0c0f\u0c2a\u0c4d\u0c30\u0c3f\u0c32\u0c4d' in dat or u'\u0c2b\u0c3f\u0c2c\u0c4d\u0c30\u0c35\u0c30\u0c3f' in dat or u'\u0c2e\u0c3e\u0c30\u0c4d\u0c1a\u0c3f' in dat or u'\u0c1c\u0c41\u0c32\u0c48' in dat:
            dat = dat.replace(u' \u0c2e\u0c47','may').replace(u'\u0c0f\u0c2a\u0c4d\u0c30\u0c3f\u0c32\u0c4d','april').replace(u'\u0c2b\u0c3f\u0c2c\u0c4d\u0c30\u0c35\u0c30\u0c3f','Feb').replace(u'\u0c2e\u0c3e\u0c30\u0c4d\u0c1a\u0c3f','March').replace(u'\u0c1c\u0c41\u0c32\u0c48','July')
        dt_added = get_timestamp(parse_date(xcode(dat)) - datetime.timedelta(hours=5, minutes=30))
        ext_link = hdoc.select('//p[@class="thumb-description black"]/a/@href').extract()
        for link in ext_link:
            if 'http' not in link: link = 'http://www.eenadu.net' + link
            yield Request(link,self.parse_details,response)


            item = Item(response)
            item.set('url', response.url)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', dt_added)
            item.set('xtags',['india_country_manual', 'news_sourcetype_manual'])
            yield item.process()
