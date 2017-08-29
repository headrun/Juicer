from juicer.utils import*
from dateutil import parser
from scrapy.http import FormRequest

class Star2(JuicerSpider):
    name = 'star2'
    start_urls = ['http://www.star2.com/']
    def parse(self,response):
        hdoc = HTML(response)
        cat_urls = hdoc.select('//a[@class="menu-link sub-menu-link"]/@href | //li[@id="nav-menu-item-133638"]/a/@href').extract()
        for cat_url in cat_urls:
            cat_url = ''.join(cat_url.split('./'))
            yield Request(cat_url, self.parse_mainlinks, response)


    def parse_mainlinks(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="row bottom-margin"]//h3')
        for node in nodes:
            date = textify(node.select('./following-sibling::span[@itemprop="dateCreated"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a/@href'))
            yield Request(link,self.parse_details,response)
        if not nodes:
            links = hdoc.select('//div[@class="article-container"]/article[@class="clearfix"]/a/@href  | //div[@class="thumb-wrap relative"]//a[@class="theme"]/preceding-sibling::a/@href').extract() or hdoc.select('//article[contains(@class, "linkbox cat-")]/a[@itemprop="url"]/@href').extract()
            for link in links:
                yield Request(link,self.parse_details,response)

            nxt_pg  = textify(hdoc.select('//a[@title="Next page"]/@href'))
            if nxt_pg:
                yield Request(nxt_pg,self.parse_mainlinks,response)

        nxt_id = textify(hdoc.select('//a[@class="next"]/@data-index'))
        post = hdoc.select('//div[@class="wpb_wrapper"]/section')
        nxt_link = 'http://www.star2.com/wp-admin/admin-ajax.php'
        headers = {'action':'miptheme_ajax_blocks', 'data_block':textify(post.select('./@data-block')),
                    'data_index':nxt_id, 'data_cat':textify(post.select('./@data-cat')),
                    'data_count':textify(post.select('./@data-count')),
                    'data_offset':textify(post.select('./@data-offset')),
                    'data_tag':'', 'data_sort':textify(post.select('./@data-sort')),
                    'data_display':'','data_text':textify(post.select('./@data-text')),
                    'data_columns':'', 'data_layout':''}
        yield FormRequest(nxt_link, self.parse_mainlinks, formdata=headers)

    def parse_details(self,response):
         hdoc = HTML(response)
         title = textify(hdoc.select('//h1[@itemprop="name"]/text()'))
         if not title:
            title = response.url.split('/')[-2].replace('-',' ')
         date = textify(hdoc.select('//p[contains(@class, "post-meta")]//span[@itemprop="dateCreated"]/text()'))
         text = textify(hdoc.select('//aside/following-sibling::p/text()')) or textify(hdoc.select('//div[contains(@class, "post-content")]//p//text()'))
         junk_text = textify(hdoc.select('//div[@class="wp-caption alignnone"]/following-sibling::p//a[@target="_blank"]/text()'))
         text = text.replace(junk_text,'')

         author = textify(hdoc.select('//div[@data-id="wid-l9nbrora"]/preceding-sibling::p[@class="post-meta clearfix"]/text()')) or textify(hdoc.select('//p[@class="post-meta clearfix"]//a[@rel="author"]/text()'))
         authr_url = textify(hdoc.select('//p[@class="post-meta clearfix"]//a[@rel="author"]/@href'))
         author = author.replace('By','').replace('\n','').replace('\t','').replace('\b','')
         dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

         item = Item(response)
         item.set('url',response.url)
         item.set('title',xcode(title))
         item.set('text',xcode(text))
         item.set('dt_added',xcode(dt_added))
         item.set('author', {'name':xcode(author)})
         item.set('author_url',xcode(authr_url))
         item.set('xtags', ['news_sourcetype_manual', 'malaysia_country_manual'])
         yield item.process()

         
