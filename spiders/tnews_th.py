from juicer.utils import*
from dateutil import parser

class Tnews(JuicerSpider):
    name = 'tnews_th'
    start_urls = ['http://www.tnews.co.th/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[contains(@class, "col-md")]/a[@target="_blank"]/@href').extract()
        for cat in categories:
            if '.tnews.co.th/allnews/FocusNew' in cat or 'http://job.tnews.co.th/' in cat:
                continue
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('///div[@class="col-md-4"]')
        for node in nodes:
            date = textify(node.select('.//small//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) -  datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//strong/a[@target="_blank"]/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//a[@rel="next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h3[@class="lh17"]//text()'))
        text = textify(hdoc.select('//p//text()')) or textify(hdoc.select('//span//text()'))
        junk_txt = textify(hdoc.select('//span[@class="sr-only"]/text()'))
        highlighted_txt = textify(hdoc.select('//h4//following-sibling::h3/strong//text()'))
        text=text.replace(junk_txt,'')
        main_text =  highlighted_txt + ' ' + text
        date =  textify(hdoc.select('//h3[@class="lh17"]//following-sibling::small//text()'))
        date =  date.replace('Publish','')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
        author = textify(hdoc.select('//footer/text()'))
        author = author.replace(':','')

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(main_text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','thailand_country_manual'])
        yield item.process()

