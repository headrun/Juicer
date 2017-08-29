from juicer.utils import *

class Yomiuri(JuicerSpider):
    name = 'yomiuri_jp'
    start_urls = ['http://www.yomiuri.co.jp/national/?from=ygnav3', 'http://www.yomiuri.co.jp/economy/?from=ygnav3', 'http://www.yomiuri.co.jp/sports/?from=ygnav3', 'http://www.yomiuri.co.jp/world/?from=ygnav3', 'http://www.yomiuri.co.jp/science/?from=ygnav3', 'http://www.yomiuri.co.jp/eco/?from=ygnav3', 'http://www.yomiuri.co.jp/culture/?from=ygnav3']

    def parse(self, response):
        hdoc = HTML(response)
        is_next = True
        threads = hdoc.select('//ul[@class="list-common"]/li[contains(@class,"no")]')

        for thread in threads:
            date = textify(thread.select('.//span[@class="update"]/text()'))
            date = '-'.join(re.findall('\w+', date))
            date_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            newslink = textify(thread.select('./a/@href'))
            yield Request(newslink, self.parse_details, response)

        nxt_pg = textify(hdoc.select('//div[@class="next"]/a/@href'))
        if nxt_pg and is_next:
            yield Request(nxt_pg, self.parse, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = xcode(textify(hdoc.select('//h1/text()')))
        dt_added = textify(hdoc.select('//div[@class="date-upper"]/time/text()')).split(' ')
        dt_added = '-'.join(re.findall('\w+', dt_added[0])) + ' ' + ':'.join(re.findall('\w+',dt_added[-1]))
        dt_added = get_timestamp(parse_date(xcode(dt_added))-datetime.timedelta(hours=9))
        text = textify(hdoc.select('//p[@itemprop="articleBody"]//text()'))

        item = Item(process)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        yield item.process()
