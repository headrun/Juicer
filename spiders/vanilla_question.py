from juicer.utils import *
from dateutil import parser

class VanillaQuestion(JuicerSpider):
    name = 'vanilla_question'
    start_urls = ['http://www.vanilla.in.th/bbs.cgi']

    def parse(self,response):
        hdoc = HTML(response)

        links = hdoc.select('//section[@id="featured"]/div[@class="topic"]/a/@href').extract()

        for link in links:
            yield Request(link,self.parse_details,response)

        next_page = textify(hdoc.select('//div[@id="pageBottom"]//i[@class="icon pagination right"]/parent::a/@href'))
        if next_page:
            yield Request(next_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//font[@class="thaiTitle"]/text()'))
        post_author = textify(hdoc.select('//section[@id="thread"]//span[@class="profile"]//a/text()'))
        post_authorurl = textify(hdoc.select('//section[@id="thread"]//span[@class="profile"]//a/@href'))
        date = ''.join(textify(hdoc.select('//section[@id="thread"]//div[@class="clearfix"]/span[not(contains(@class,"*"))]/text()')).split('Room :')[-1])
        dt_added = parse_date(xcode(date))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
        if dt_added >= get_current_timestamp()-86400*30:
            other_info = textify(hdoc.select('//section[@id="thread"]//span[@class="hide-phone"]//text()')).strip('|')
            text = textify(hdoc.select('//section[@id="thread"]//span[@class="thaiSTD"]//text()'))

            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('author',{'name':xcode(post_author),'url':post_authorurl,'other_information':xcode(other_info)})
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('xtags',['thailand_country_manual','reviews_sourcetype_manual'])
            yield item.process()

            nodes = hdoc.select('//section[@id="post-comment"]//div[@class="user-message-big clearfix"]')
            for node in nodes:
                author_name = textify(node.select('.//span[@class="profile"]//a/text()'))
                author_url = textify(node.select('.//span[@class="profile"]//a/@href'))
                other_details = textify(node.select('.//span[@class="profile"]//span[@class="hide-phone"]//text()')).strip('|')
                dt = textify(node.select('.//div[@class="clearfix"]/span[not(contains(@class,"*"))]/text()'))
                date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=7))
                text1 = textify(node.select('.//span[@class="thaiSTD"]//text()'))
                sk = xcode(author_name) + str(dt_added) + xcode(text1)

                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('author',{'name':xcode(author_name),'url':author_url,'other_information':xcode(other_details)})
                item.set('dt_added',date_added)
                item.set('text',xcode(text1))
                item.set('sk',md5(sk))
                item.set('xtags',['thailand_country_manual','reviews_sourcetype_manual'])
                yield item.process()
