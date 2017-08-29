from juicer.utils import*
from dateutil import parser

class Sinarharian_MY(JuicerSpider):
    name = 'sinarharian_my'
    start_urls = ['http://www.sinarharian.com.my/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="header-two-area "]//li/a/@href | //div[@class="xtra-menu"]/a/@href').extract()
        for cate in categories:
            if 'http' not in cate: cate = 'http://www.sinarharian.com.my' + cate
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="element teaser"]')
        for node in nodes:
            date=textify(node.select('.//div[@class]//text()'))
            if not date:
            date = ''.join(re.findall('var dateEG = "(.*?)"',date))

            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            link = textify(node.select('.//div[@class]//a[not(img)]/@href'))
            if 'http' not in link: link = 'http://www.sinarharian.com.my' + link

            import pdb;pdb.set_trace()
