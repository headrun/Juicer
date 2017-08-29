from juicer.utils import *
class Honda(JuicerSpider):
    name = "get"
    start_urls = "https://get.com/"


    def parse(self,response):
        hdoc = HTML(response)

        urls = hdoc.select('//div[@class="block-links"]//li//a/@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
        urls = hdoc.select('//ul[@class="dropdown"]//li//a/@href')
        import pdb;pdb.set_trace()
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//header[@class="article_header large-24 columns "]//h1'))
        text = textify(hdoc.select('//div[@class="content  large-24 columns "]//p'))
        date = textify(hdoc.select('//p[@class="hide-for-small-only updated-date"]//time'))
        author = textify(hdoc.select('//div[@class="article_author left"]//a'))
        date = get_timestamp(parse_date(date) + datetime.timedelta(hours=8))
"""
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('url', response.url)
        item.set('author.name', author.strip())
        item.set('dt_added', date)
        item.set('xtags', ['usa_country_manual', 'capitalone_project_manual', 'news_sourcetype_manual'])

        if author:
            yield item.process()
"""
