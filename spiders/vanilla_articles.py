from juicer.utils import *
from dateutil import parser

class VanillaArticles(JuicerSpider):
    name  = 'vanilla_articles'
    start_urls = ['http://www.vanilla.in.th/activities/top','http://www.vanilla.in.th/topic_list.cgi?id=009']

    def parse(self,response):
        hdoc = HTML(response)

        links = hdoc.select('//ul[@id="featured"]//div[@class="caption"]/a/@href | //li[@class="actinfo"]/a/@href').extract()

        for link in links:
            if 'http' not in link: link = 'http://www.vanilla.in.th' + link
            yield Request(link,self.parse_details,response)

        next_page = textify( hdoc.select('//div[@id="pageBottom"]//i[@class="icon pagination right"]/parent::a/@href')).strip('.')
        if next_page:
            next_page = 'http://www.vanilla.in.th' + next_page
            yield Request(next_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        complete_title = textify(hdoc.select('//h4[@class="title-underline3"]//text()'))
        title = textify(hdoc.select('//font[@class="thaiTitle"]/text()'))
        date = ''.join(textify(hdoc.select('//div[@class="update"]/text()')).split('Update :')[-1])
        dt_added = parse_date(xcode(date))
        text = textify(hdoc.select('//span[@class="thaiSTD pr"]//p//text() | //span[@class="thaiSTD_act"]//p//text()'))
        if  u'\u0e01\u0e15\u0e34\u0e01\u0e32' in text: text = textify(text.split(u'\u0e01\u0e15\u0e34\u0e01\u0e32')[0])

        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
        if dt_added > get_current_timestamp()-86400*30:
            item = Item(response)
            item.set('url',response.url)
            item.set('complete_title',xcode(complete_title))
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('xtags',['news_sourcetype_manual','thailand_country_manual'])
            yield item.process()

            nodes = hdoc.select('//div[@class="user-message-big clearfix"]')

            for node in nodes:
                author_name = textify(node.select('.//span[@class="profile"]/span/a/text()'))
                author_url = textify(node.select('.//span[@class="profile"]/span/a/@href'))
                if 'http' not in author_url: author_url = 'http://www.vanilla.in.th/' + author_url
                author_info = textify(node.select('.//span[@class="hide-phone"]//text()')).strip('|')
                dt = textify(node.select('.//div[@class="commenterinfo"]/span[not(contains(@class,"*"))]/text()'))
                dt_added1 = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=7))
                comment = textify(node.select('.//div[@class="message thaiSTD"]/p//text()'))

                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('author',{'name':xcode(author_name),'url':author_url,'_info':xcode(author_info)})
                item.set('dt_added',dt_added1)
                item.set('text',xcode(comment))
                item.set('xtags',['newss_sourcetype_manual','thailand_country_manual'])
                yield item.process()
