from juicer.utils import*
from dateutil import parser
class DiabeticConnect_USA(JuicerSpider):
    name = 'diabetic_connect'
    start_urls = ['http://www.diabeticconnect.com/diabetes-discussions']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="dropdown-menu"]/li[@class="divider"]/following-sibling::li/a/@href').extract()
        for cat in categories:
            if 'http://www.attentiondeficitconnect.com' in cat or 'http://www.anxietyconnect.com' in cat or 'http://www.bipolardisorderconnect.com' in cat or 'http://www.depressionconnect.com' in cat:
                continue
            yield Request(cat,self.parse_subcategories,response)

    def parse_subcategories(self,response):
        hdoc = HTML(response)
        nodes_categories = hdoc.select('//li[@class="thread-bubble"]')
        for node in nodes_categories:
            date = textify(node.select('.//span[@class="-format-time"]/text()'))
            date = date.split(' -')[0]
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            link = textify(node.select('.//header/h3/a/@href'))
            if 'http' not in link: link = 'http://www.diabeticconnect.com' + link
            if date_added < get_current_timestamp()-86400*30:
                yield Request(link,self.parse_threads,response)
        nxt_pg = textify(hdoc.select('//div[@class="pagination"]/a[@class="next_page"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.diabeticconnect.com' + nxt_pg
        if nxt_pg:
            yield Request(nxt_pg,self.parse_subcategories,response)

    def parse_threads(self,response):
        hdoc = HTML(response)
        forum = response.url
        nodes = hdoc.select('//article[@class="post-format"]')
        for node in nodes:
            main_thread_date = textify(node.select('.//span[@class="i-link time"]/span[@class="-format-time"]/text()'))
            main_thread_date = main_thread_date.split(' -')[0]
            main_dt_added = get_timestamp(parse_date(xcode(main_thread_date)) - datetime.timedelta(hours=8))
            if main_dt_added < get_current_timestamp()-86400*30:
                main_thread_text = textify(node.select('.//div[@class="body"]//text()'))
                main_thread_title = textify(node.select('.//h1[@class="title"]/text()'))
                main_thread_text = textify(node.select('.//div[@class="body"]//text()'))
                main_thread_author = textify(node.select('.//span[@class="i-link starter"]/span[@class="user-link"]/a/text()'))
                main_thread_author_link = textify(node.select('//span[@class="i-link starter"]/span[@class="user-link"]/a/@href'))
                if 'http' not in main_thread_author_link: main_thread_author_link = 'http://www.diabeticconnect.com' + main_thread_author_link
                main_thread_id = textify(re.findall('/(\d+)-', response.url))
                thread = {'url':response.url,'title':main_thread_title,'id':main_thread_id}
                
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(main_thread_title))
                item.set('text',xcode(main_thread_text))
                item.set('author',xcode(main_thread_author))
                item.set('author_link',xcode(main_thread_author_link))
                item.set('dt_added',xcode(main_dt_added))
                item.set('forum',forum)
                item.set('thread',thread)
                item.set('xtags',['forums_sourcetype_manual','usa_country_manual'])
                yield item.process() 

                comments = hdoc.select('//section[@class="comments"]/header[@class="dotted-with-floater"]/following-sibling::article//div[@class="discussion-body"]')
                for comment in comments:
                    comment_url = textify(comment.select('./header/span/a/@href'))
                    if 'http' not in comment_url: comment_url = 'http://www.diabeticconnect.com' + comment_url
                    sk = comment_url
                    comment_id = textify(re.findall('/(\d+)-', comment_url))
                    comment_date = textify(comment.select('.//span[@class="time"]/span/text()'))
                    comment_date = comment_date.split(' -')[0]
                    dt_added = get_timestamp(parse_date(xcode(comment_date)) - datetime.timedelta(hours=8))
                    comment_text = textify(comment.select('.//div[@class="contents"]//text()'))
                    comment_author = textify(comment.select('.//span[@class="user-link"]/a/text()'))
                    comment_author_link = textify(comment.select('.//span[@class="user-link"]/a/@href'))
                    if 'http' not in comment_author_link: comment_author_link = 'http://www.diabeticconnect.com' + comment_author_link
                    Reply = {'url':comment_url,'title':main_thread_title,'id':comment_id}
            
        
                    item = Item(response)
                    item.set('url',response.url)
                    item.set('title',xcode(main_thread_title))
                    item.set('text',xcode(comment_text))
                    item.set('author',xcode(comment_author))
                    item.set('author_link',xcode(comment_author_link))
                    item.set('dt_added',xcode(dt_added))
                    item.set('Reply',Reply)
                    item.set('sk',sk)
                    item.set('xtags',['forums_sourcetype_manual','usa_country_manual'])
                    yield item.process() 
                    
            

        additional_thread= textify(hdoc.select('//div[@class="next-discussion"]//strong/a/@href'))
        if additional_thread:
            yield Request(additional_thread,self.parse_threads,response)
