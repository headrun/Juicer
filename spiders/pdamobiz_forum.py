from juicer.utils import *
from dateutil import parser

class Pdamobizforum(JuicerSpider):
    name = "pdamobiz_forum"
    start_urls = ['http://www.pdamobiz.com/forum/']

    def parse(self,response):
        hdoc = HTML(response)

        nodes = hdoc.select('//td[@class="text"]/a/@href').extract()
        for node in nodes:
            if 'http' not in node: node = 'http://www.pdamobiz.com/forum/' + node
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        forum_id = response.url.split('FID=')[1]
        forum_name = xcode(textify(hdoc.select('//td[@class="heading"]/text()')))
        forum = {'url':response.url,'id':forum_id,'name':forum_name}
        threadlinks = hdoc.select('//tr/td[@class="smText"]')
        for threadlink in threadlinks:
            thread_link = textify(threadlink.select('./a[contains(@href,"forum_posts")]/@href'))
            if 'http' not in thread_link and thread_link: thread_link = 'http://www.pdamobiz.com/forum/' + thread_link

            if thread_link:
                date1 = textify(threadlink.select('./text()')).split(' ')[0]
                date_added = get_timestamp(parse_date(xcode(date1)) - datetime.timedelta(hours=7))

                if date_added < get_current_timestamp()-86400*30:
                    is_next = False
                    continue
                yield Request(thread_link,self.parse_details,response,meta={'forum':forum})

        next_page = textify(hdoc.select('//td[@class="text"]/a[contains(@href,"&PN=")]/@href').extract()[-1])
        if next_page and is_next:
            next_page = 'http://www.pdamobiz.com/forum/' + next_page
            yield Request(next_page,self.parse_next,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        thread_name = textify(hdoc.select('//td[@class="tHeading"]/text()'))
        thread_id = textify(response.url.split('TID=')[-1]).split('&')[0]
        comments = hdoc.select('//table//tr/td/a[@name]')
        for comment in comments:
            author = textify(comment.select('./parent::td[@class="bold"]/text()'))
            if author:
                date = textify(comment.select('./parent::td[@class="bold"]/following-sibling::td//td[@class="smText"]/text()')).split(' ')
                date = parse_date(xcode(date[0] + ' ' + date[2]))
                dt_added = get_timestamp(date,dayfirst=True) - datetime.timedelta(hours=7))
                _id = textify(comment.select('./@name'))
                text = textify(comment.select('./parent::td[@class="bold"]/parent::tr/following-sibling::tr[1]/td[@class="text"]//text()'))
                other_info = comment.select('./parent::td[@class="bold"]/parent::tr/following-sibling::tr[1]/td[@class="smText"]//text()').extract()
                other_info = ','.join(str(xcode(i)).strip(' ') for i in other_info)
                if date < get_current_timestamp()-86400*30:
                    is_next = False
                    continue

                item = Item(process)
                item.set('url',response.url +'#' +_id)
                item.set('title',xcode(thread_name))
                item.set('author',{'name':xcode(author),'other_info':xcode(other_info)})
                item.set('dt_added',dt_added)
                item.set('text',xcode(text))
                item.set('forum',response.meta['forum'])
                item.set('thread',{'name':xcode(thread_name),'url':response.url,'id':thread_id})
                item.set('xtags',['forums_sourcetype_manual','thailand_country_manual'])
                yield item.process()

        try:nxt_pg = textify(hdoc.select('//select[@name="SelectTopicPage"]/option[@selected]/preceding-sibling::option/@value').extract()[-1])
        except:nxt_pg = ''
        if nxt_pg != '' and is_next:
            nxt_pg = 'http://www.pdamobiz.com/forum/' + nxt_pg
            yield Request(nxt_pg,self.parse_details,response,meta={'forum':response.meta['forum']})
