from juicer.utils import*
from dateutil import parser

class Htsyndication_IN(JuicerSpider):
    name = 'htsyndication'
    start_urls = ['http://htsyndication.com/htsportal/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav footer-nav"]//li/a[contains(@href, "category")]/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://htsyndication.com' + cat
            yield Request(cat,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="col-xs-12 col-sm-9 col-md-9 col-lg-9"]/h1/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://htsyndication.com' + link
            yield Request(link,self.parse_details,response)

        next_page = hdoc.select('//ul[@class="pagination"]//li/a[contains(.,"%s")]/@href'%u'\xbb').extract()
        if next_page:
            nxt_pg = ''.join(hdoc.select('//ul[@class="pagination"]//li/a[contains(.,"%s")]/@href'%u'\xbb').extract()[0])
            if 'http' not in nxt_pg: nxt_pg = 'http://htsyndication.com' + nxt_pg
            if nxt_pg:
                yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
"""
        nodes = hdoc.select('//h1')
        for node in nodes:
            date = textify(node.select('./following-sibling::div[@class="article-meta clearfix"]//span[@class="badge"]//text()'))
            link = textify(node.select('./a/@href'))
            import pdb;pdb.set_trace()
            """
