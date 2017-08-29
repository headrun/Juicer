from juicer.utils import *
from dateutil import parser

class Nfpeople(JuicerSpider):
    name = "nfpeople_china"
    start_urls = ['http://www.nfpeople.com/cate.php?dir=news','http://www.nfpeople.com/cate.php?dir=cover','http://www.nfpeople.com/cate.php?dir=topic','http://www.nfpeople.com/cate.php?dir=bussines','http://www.nfpeople.com/cate.php?dir=culture','http://www.nfpeople.com/cate.php?dir=sport','http://www.nfpeople.com/cate.php?dir=celebrity','http://www.nfpeople.com/cate.php?dir=column','http://www.nfpeople.com/cate.php?dir=album','http://www.nfpeople.com/cate.php?dir=review','http://www.nfpeople.com/cate.php?dir=people','http://www.nfpeople.com/cate.php?dir=life','http://www.nfpeople.com/cate.php?dir=guandian','http://www.nfpeople.com/cate.php?dir=tegao','http://www.nfpeople.com/cate.php?dir=picstory','http://www.nfpeople.com/cate.php?dir=relatednews','http://www.nfpeople.com/cate.php?dir=cooperationpress','http://www.nfpeople.com/cate.php?dir=across','http://www.nfpeople.com/cate.php?dir=report','http://www.nfpeople.com/cate.php?dir=nonfiction','http://www.nfpeople.com/cate.php?dir=fiction','http://www.nfpeople.com/cate.php?dir=history','http://www.nfpeople.com/cate.php?dir=sjg','http://www.nfpeople.com/cate.php?dir=datanews','http://www.nfpeople.com/cate.php?dir=zyzy','http://www.nfpeople.com/cate.php?dir=xinzhixz','http://www.nfpeople.com/cate.php?dir=qaqaqa','http://www.nfpeople.com/cate.php?dir=scjscj','http://www.nfpeople.com/cate.php?dir=jsjsjs','http://www.nfpeople.com/cate.php?dir=mxmxmx','http://www.nfpeople.com/cate.php?dir=yzgzyzgz','http://www.nfpeople.com/cate.php?dir=dldl','http://www.nfpeople.com/cate.php?dir=ytdytd','http://www.nfpeople.com/cate.php?dir=yxyxyx','http://www.nfpeople.com/cate.php?dir=xsxsx','http://www.nfpeople.com/cate.php?dir=szszs','http://www.nfpeople.com/cate.php?dir=scqhscqh','http://www.nfpeople.com/cate.php?dir=grsgrs','http://www.nfpeople.com/cate.php?dir=fshfsh','http://www.nfpeople.com/cate.php?dir=sdzhsdzh','http://www.nfpeople.com/cate.php?dir=kjkj','http://www.nfpeople.com/cate.php?dir=shizhe','http://www.nfpeople.com/cate.php?dir=shyshy']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="leftbox lists"]//dl//dt//a//@href')
        import pdb;pdb.set_trace()
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc =HTML(response)
        title = textify(hdoc.select('//center//h1//text()'))
        text = textify(hdoc.select('//div[@class="mainContent"]/p/text()'))
        dt_added = textify(hdoc.select('//center//p[@class="source"]//text()'))
        dt_added = dt_added.split(u'\uff1a')
        dt_added = dt_added[3]
        author = textify(hdoc.select('//center//p[@class="source"]//text()'))
        author = author.split('  ')
        author = author[2]
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
'''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()'''
