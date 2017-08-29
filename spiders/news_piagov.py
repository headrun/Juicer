from juicer.utils import*
from dateutil import parser

class News_piagovPH(JuicerSpider):
    name = 'news_piagov'
    start_urls = ['http://news.pia.gov.ph/regional/CENTRAL']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[@class="mega-menu-dropdown"]/a/@href | //ul[@class="col-md-4 mega-menu-submenu"]/li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)
        cates = ['http://pia.gov.ph/blog/welcome/reflections', 'http://pia.gov.ph/blog/welcome/features']
        for cate in cates:
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="well margin-bottom-10"] | //div[@class="blog-post"]')
        for node in nodes:
            link = textify(node.select('./h4/a/@href | ./h2/a/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = hdoc.select('//ul[@class="pagination"]/li//a//@href').extract()[-2] or textify(hdoc.select('//ul[@class="pagination"]/li/a[@rel="next"]/@href'))
        if nxt_pg :
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        date = textify(hdoc.select('//ul[@class="post-meta"]/li//text()')) or textify(hdoc.select('//i[@class="fa fa-user"]//preceding::li[1]/text()'))

        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

        title = textify(hdoc.select('//h1/text()')) or textify(hdoc.select('//h3[@class="page-title"]/b/text()'))
        text = textify(hdoc.select('//div[@class="col-md-12"]//p//text()')) or textify(hdoc.select('//div[@class="post-desc"]//p//text()')) or textify(hdoc.select('//div[contains(@id, "yiv")]//text()')) or textify(hdoc.select('//div[@class="col-md-12 margin-bottom-10"]/div[@class="col-md-12"]//text()'))
        author = textify(hdoc.select('//div[@class="post-desc"]/p/em/text()')) or textify(hdoc.select('//li[i[@class="fa fa-user"]]//text()'))
        author = author.replace('By','')

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','philippines_country_manual'])
        yield item.process()

