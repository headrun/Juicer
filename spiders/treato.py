from juicer.utils import *
from dateutil import parser

class Drugs(JuicerSpider):
    name = 'treato'
    start_urls = ['http://treato.com/sitemap/drugs']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        alphabets = hdoc.select('//ul//li/a/@href').extract()
        for alphabet in alphabets:
            alpha_url = 'http://treato.com' + alphabet
            yield Request(alpha_url,self.category,response)

    def category(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul/following-sibling::a/@href').extract()
        for cat in categories:
            cat_url = 'http://treato.com' + cat
            yield Request(cat_url,self.sub_category,response)

    def sub_category(self,response):
        hdoc = HTML(response)
        sub_cats =  hdoc.select('//a/@href').extract()
        for sub_cat in sub_cats:
            sub_cat_url = 'http://treato.com' + sub_cat

            if '/?a=s' in sub_cat_url:
                yield Request(sub_cat_url,self.details,response)
            else:
                yield Request(sub_cat_url,self.sub_category,response)

    def details(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="column large-12 no-padding"]//a/@href').extract()

        for node in nodes:
            node_url = 'http://treato.com' + node
            yield Request(node_url,self.posts,response)

    def posts(self,response):
        hdoc = HTML(response)
        is_next = True
        exp_title =  textify(hdoc.select('//div[@class="row"]/h2//text()'))
        medicine_title = textify(hdoc.select('//div[@class="row"]/h1//text()'))
        post_user =  hdoc.select('//div[@class="post-wrap"]')
        if exp_title:
            title = exp_title
        else:
            title = medicine_title
        for post in post_user:
            date = textify(post.select('.//div[@class="post-timestamp"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=-5))
            if dt_added < get_current_timestamp()-86400*90 or not date:
                is_next = False
                continue
            user = textify(post.select('.//div[@class="user-name"]/text()'))
            text = textify(post.select('.//div[@class="post-content"]//text()'))
            sk = response.url+title+text

            item = Item(response)
            item.set('url',response.url)
            item.set('title',title)
            item.set('author.name',user)
            item.set('dt_added',dt_added)
            item.set('text',text)
            item.set('sk',md5(sk))
            item.set('xtags',['forums_sourcetype_manual','usa_country_manual'])
            yield item.process()


        medicines = hdoc.select('//div[@class="column large-9 medium-9 small-9"]/a/@href').extract()
        for medicine in medicines:
            medicine_url = 'http://treato.com' + medicine
            yield Request(medicine_url,self.posts,response)

        nxt_pg = textify(hdoc.select('//div[@class="posts-pager"]/a[@class="pager-next"]/@href')[0])
        if nxt_pg and is_next:
            nxt_pg_url = 'http://treato.com' + nxt_pg
            yield Request(nxt_pg_url,self.posts,response)
