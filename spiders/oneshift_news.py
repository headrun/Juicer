from juicer.utils import *
from scrapy.http import FormRequest
from lxml import etree
import urllib2

class OneshitReviews(JuicerSpider):
    name = 'oneshift_reviews'
    start_urls = 'http://www.oneshift.com/articles/ajax_load_articles.php'

    def parse(self,response):
        hdoc = HTML(response)
        newslinks = hdoc.select('//div[@class="div_roadtest_title_container"]/a/@href').extract()
        for newslink in newslinks:
            yield Request(newslink,self.details,response)

        session_ids = ['4+5+6+7+9+10+11+12+14+18+23', '1']
        try:page_id = int(response.meta['page_id']) + 1
        except:page_id = 0
        for ids in session_ids:
            headers = {'sectionid':ids,
                        'pageid':str(page_id) }
            yield FormRequest(response.url,callback=self.parse,meta={'page_id':page_id},formdata=headers)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//title/text()'))
        author = textify(hdoc.select('//span[@itemprop="reviewer"]'))or textify(hdoc.select('//div[@class="div_nf_author12 author"]/text()')) or textify(hdoc.select('//div[@class="article_author"]/text()')).strip('-').strip(' ')
        if 'by' in author:
            author = author.split('by')[-1].strip('-').strip(' ')
        date = textify(hdoc.select('//span[@datetime]/text()'))
        dt_added = get_timestamp(parse_date(xcode(str(date)))-datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[contains(@class,"div_nf_content")]//text()')) or textify(hdoc.select('//div[@itemprop="description"]//text()')) or textify(hdoc.select('//div[@class="article"]//text()'))
        if text =='':import pdb;pdb.set_trace()
        nxt_pg = textify(hdoc.select('//span[@class="nextPage"]/a/@href'))
        if nxt_pg:
            extra_text = urllib2.urlopen(nxt_pg).read()
            extra_text = etree.HTML(extra_text)
            text2 = textify(extra_text.xpath('//div[contains(@class,"div_nf_content")]//text()'))
            text = text + text2

        if dt_added > get_current_timestamp()-86400*30:
            if title != '' or text != '' :
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('dt_added',dt_added)
                item.set('author',{'name':xcode(author)}
                item.set('text',xcode(text))
