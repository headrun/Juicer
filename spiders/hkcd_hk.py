from juicer.utils import *
from dateutil import parser

class Hkcd(JuicerSpider):
    name = 'hkcd_hk'
    start_urls = ['http://www.hkcd.com/node_6.html','http://www.hkcd.com/node_7.html','http://www.hkcd.com/node_4.html','http://www.hkcd.com/node_5.html','http://www.hkcd.com/node_8.html','http://www.hkcd.com/node_9.html','http://www.hkcd.com/node_10.html','http://www.hkcd.com/node_11.html','http://www.hkcd.com/node_12.html','http://www.hkcd.com/node_13.html','http://www.hkcd.com/node_14.html','http://www.hkcd.com/node_15.html','http://www.hkcd.com/node_51.html','http://www.hkcd.com/node_52.html','http://www.hkcd.com/node_60.html','http://www.hkcd.com/node_86.html','http://www.hkcd.com/node_46.html','http://www.hkcd.com/node_40.html','http://www.hkcd.com/node_85.html','http://www.hkcd.com/node_83.html','http://www.hkcd.com/node_84.html','http://www.hkcd.com/node_41.html','http://www.hkcd.com/node_32.html','http://www.hkcd.com/node_102.html','http://www.hkcd.com/node_62.html','http://www.hkcd.com/node_57.html','http://www.hkcd.com/node_58.html','http://www.hkcd.com/node_60.html','http://www.hkcd.com/node_59.html','http://www.hkcd.com/node_61.html','http://www.hkcd.com/node_96.html','http://www.hkcd.com/node_50.html','http://www.hkcd.com/node_25.html','http://www.hkcd.com/node_24.html','http://www.hkcd.com/node_27.html','http://www.hkcd.com/node_55.html','http://www.hkcd.com/node_26.html','http://www.hkcd.com/node_72.html','http://www.hkcd.com/node_37.html','http://www.hkcd.com/node_77.html','http://www.hkcd.com/node_78.html','http://www.hkcd.com/node_104.html','http://www.hkcd.com/node_183.html','http://www.hkcd.com/node_254.html','http://www.hkcd.com/node_256.html','http://www.hkcd.com/node_93.html','http://www.hkcd.com/node_90.html','http://www.hkcd.com/head_list.html']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="cat_new_zs cat_newlist"]/ul/li')
        for node in nodes:
            dt = textify(node.select('./span/text()')).strip('()')
            dtadded = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            import pdb;pdb.set_trace()
            if dtadded < get_current_timestamp()-86400*30:
                is_next = False
                continue
            url = textify(node.select('./a/@href'))
            if 'http' not in url: url = 'http://www.hkcd.com/' + url
            yield Request(url,self.parse_details,response)

        nxt_pages = hdoc.select("//ul[@class='fenye_ul']/li/a/@href").extract()
        for nxt_page in nxt_pages:
            if nxt_page and is_next:
                nxt_page = 'http://www.hkcd.com/' + nxt_page
                yield Request(nxt_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="conten_title"]/text()'))
        date = textify(hdoc.select('//span[@class="ti_l"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="author"]/text()')).split(u'\uff1a')[-1].strip(']')
        text = textify(hdoc.select('//div[@class="content_main"]/p//text()'))

        """item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title)
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('text',xcode(text))
        yield item.process()"""
