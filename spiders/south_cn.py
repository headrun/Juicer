from juicer.utils import *
from dateutil import parser

class SouthCn(JuicerSpider):
    name = "south_cn"
    start_urls = ['http://news.southcn.com/china/','http://news.southcn.com/community/','http://news.southcn.com/international/','http://news.southcn.com/gd/','http://news.southcn.com/sj/','http://news.southcn.com/fu/','http://news.southcn.com/dishi/jdht/node_288371.htm','http://news.southcn.com/dishi/phb/node_288771.htm','http://news.southcn.com/dishi/gdhd/node_288772.htm','http://news.southcn.com/dishi/dszt/node_288773.htm','http://news.southcn.com/sd/','http://news.southcn.com/py/','http://economy.southcn.com/node_165833.htm','http://economy.southcn.com/node_165832.htm','http://economy.southcn.com/node_165834.htm','http://economy.southcn.com/node_165812.htm','http://economy.southcn.com/node_165813.htm','http://economy.southcn.com/node_165826.htm','http://economy.southcn.com/node_165811.htm','http://opinion.southcn.com/o/node_82374.htm','http://opinion.southcn.com/o/node_96066.htm','http://opinion.southcn.com/o/node_292573.htm','http://opinion.southcn.com/o/node_292572.htm','http://opinion.southcn.com/o/node_105814.htm','http://opinion.southcn.com/o/node_96464.htm','http://opinion.southcn.com/o/node_82377.htm','http://opinion.southcn.com/o/node_78586.htm','http://opinion.southcn.com/o/node_82376.htm','http://opinion.southcn.com/o/node_78585.htm','http://finance.southcn.com/f/node_123274.htm','http://finance.southcn.com/zqsc/node_189033.htm','http://finance.southcn.com/lccp/node_189031.htm','http://finance.southcn.com/jjhq/node_189034.htm','http://finance.southcn.com/bxzx/node_189035.htm','http://finance.southcn.com/tzsc/node_189611.htm','http://finance.southcn.com/cpts/node_189037.htm','http://finance.southcn.com/hjwh/node_189042.htm','http://finance.southcn.com/qhqz/node_189045.htm','http://finance.southcn.com/ssgs/node_189041.htm','http://finance.southcn.com/hygg/node_189048.htm','http://news.southcn.com/zhuanti/','http://lady.southcn.com/6/node_83952.htm','http://lady.southcn.com/6/node_83972.htm','http://lady.southcn.com/6/node_83954.htm','http://lady.southcn.com/6/node_83936.htm','http://lady.southcn.com/6/node_83935.htm','http://ent.southcn.com/8/node_146912.htm','http://ent.southcn.com/8/node_85545.htm','http://ent.southcn.com/8/node_138812.htm','http://ent.southcn.com/yulun/yulunying/default.htm','http://ent.southcn.com/8/node_86097.htm','http://ent.southcn.com/zhuanti/tvtuijian/default.htm','http://ent.southcn.com/8/node_134551.htm','http://ent.southcn.com/8/haiw/node_304251.htm','http://tech.southcn.com/t/node_104011.htm','http://tech.southcn.com/t/node_193171.htm','http://tech.southcn.com/t/node_103962.htm','http://tech.southcn.com/t/node_103959.htm','http://tech.southcn.com/t/node_213248.htm','http://tech.southcn.com/t/node_103957.htm','http://tech.southcn.com/t/node_103963.htm','http://tech.southcn.com/t/node_114419.htm','http://tech.southcn.com/t/node_103955.htm','http://tech.southcn.com/t/node_103958.htm','http://car.southcn.com/7/node_114251.htm','http://life.southcn.com/g/node_273468.htm']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="pw"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="time"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h3/a[@target="_blank"]/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@id="displaypagenum"]//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title=textify(hdoc.select('//h2[@id="article_title"]//text()')) or textify(hdoc.select('//h1[@id="article_title"]//text()'))

        text=textify(hdoc.select('//div[@class="content"]//p//text()'))
        date=textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="m-editor"]//text()'))
        author = author.replace(u'\u7f16\u8f91','')
        author = author.replace(u'\uff1a\r\n\t\t\t\t','')
        next_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if next_pg:
            yield Request(next_pg,self.parse_details,response)

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()



