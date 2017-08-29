from juicer.utils import*
from dateutil import parser

class Stomp_straittimes(JuicerSpider):
    name = 'stomp_straittimes'
    start_urls = ['http://stomp.straitstimes.com/singapore-seen?page=0']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="view-content"]//h3/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://stomp.straitstimes.com' + nxt_pg
        yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="headline"]//text()')) or textify(hdoc.select('//div[@class="field-item even"]/h1/text()')) or textify(hdoc.select('//header/h2//text()'))
        text = textify(hdoc.select('//div[@class="field-item even"]//p[not(em)]//text()'))
        junk_txt = textify(hdoc.select('//div[@class="text"]//p//text()'))
        text = text.replace(junk_txt,'')
        date = textify(hdoc.select('//div[@class="submitted"]//text()'))
        date=date.split('|')[0].replace('Posted on ','')
        if not date:
            dt = textify(hdoc.select('//span[@property="dc:date dc:created"]/@content'))
            date = ''.join(re.findall('(.*)\T',dt))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="group-ob-wrapper field-group-div ob-readmore-collapse"]/p/strong[a]//text()')) or textify(hdoc.select('//span[@class="username"]'))
        author_url = textify(hdoc.select('//div[@class="group-ob-wrapper field-group-div ob-readmore-collapse"]/p/strong[a]//@href'))
        if 'http' not in author_url: author_url = 'http://stomp.straitstimes.com' + author_url

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags', ['news_sourcetype_manual', 'singapore_country_manual'])
        yield item.process()
