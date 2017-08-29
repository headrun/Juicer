from juicer.utils import *
from dateutil import parser

class OzbargainForum(JuicerSpider):
    name = 'ozbargain_forum'
    start_urls = ['https://www.ozbargain.com.au/forum/30','https://www.ozbargain.com.au/forum/38181','https://www.ozbargain.com.au/forum/538','https://www.ozbargain.com.au/forum/38182','https://www.ozbargain.com.au/forum/546','https://www.ozbargain.com.au/forum/38183','https://www.ozbargain.com.au/forum/500','https://www.ozbargain.com.au/forum/40715','https://www.ozbargain.com.au/forum/505','https://www.ozbargain.com.au/forum/42','https://www.ozbargain.com.au/forum/50999','https://www.ozbargain.com.au/forum/38184','https://www.ozbargain.com.au/forum/533','https://www.ozbargain.com.au/forum/38185','https://www.ozbargain.com.au/forum/7','https://www.ozbargain.com.au/forum/23834','https://www.ozbargain.com.au/forum/30381','https://www.ozbargain.com.au/forum/1341','https://www.ozbargain.com.au/forum/5','https://www.ozbargain.com.au/forum/68']

    def parse(self,response):
        hdoc = HTML(response)
        forum_name = textify(hdoc.select('//h1[@id="title"]/text()')).split(u'\xbb')[0]
        if 'page=' not in response.url:forum_id = response.url.split('forum/')[-1]
        else:forum_id = textify(response.url.split('forum/')[-1]).split('?page=')[0]
        forum = {'name':forum_name,'id':forum_id,'url':response.url}
        links = hdoc.select('//table[@class="forum-topics"]/tbody/tr')

        for link in links:
            date = textify(link.select('./td[@class="last-reply"]/div/text()'))
            date_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                continue
            threadlink= textify(link.select('./td[@class="topic"]/span[@class="title"]/a/@href'))
            if 'http' not in threadlink: threadlink = 'https://www.ozbargain.com.au' + threadlink
            yield Request(threadlink,self.parse_details,response,meta={'forum':forum})

        next_page = textify(hdoc.select('//li/a[@title="Go to next page"]/@href'))
        if 'http' not in next_page:next_page = 'https://www.ozbargain.com.au' + next_page
        yield Request(next_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="title"]/span[@class="title"]/text()'))
        thread_id = response.url.split('node/')[-1]
        text = textify(hdoc.select('//div[@class="node node-forum"]//div[@class="content"]//text()'))
        post_author = textify(hdoc.select('//div[@class="node node-forum"]//div[@class="submitted"]//a[@title="View user profile."]/text()'))
        post_authorurl = textify(hdoc.select('//div[@class="node node-forum"]//div[@class="submitted"]//a[@title="View user profile."]/@href'))
        if 'http' not in post_authorurl: post_authorurl = 'https://www.ozbargain.com.au' + post_authorurl
        dt = textify(hdoc.select('//div[@class="node node-forum"]//div[@class="submitted"]/text()')).split('Last')[0].strip('on')
        dt_added = get_timestamp(parse_date(xcode(dt),dayfirst=True) - datetime.timedelta(hours=10))
        if dt_added >= get_current_timestamp()-86400*30:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('author',{'name':post_author,'url':post_authorurl})
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('forum',response.meta['forum'])
            item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
            yield item.process()

        nodes = hdoc.select('//div[@class="comment-wrap"]/div[contains(@class,"comment")]')
        for node in nodes:
            author_name = textify(node.select('.//a[@title="View user profile."]/text()'))
            author_url = textify(node.select('.//a[@title="View user profile."]/@href'))
            if 'http' not in author_url: author_url = 'https://www.ozbargain.com.au' + author_url
            comment_id = textify(node.select('.//div/@data-cid'))
            dt1 = textify(node.select('.//div[@class="submitted"]/a/text()'))
            dt_added1 = get_timestamp(parse_date(xcode(dt1),dayfirst=True) - datetime.timedelta(hours=10))
            comment = textify(node.select('.//div[@class="content"]//text()'))
            sk = response.url + '#comment-' + comment_id
            if dt_added >= get_current_timestamp()-86400*30:
                item = Item(response)
                item.set('url',response.url + '#comment-' + comment_id)
                item.set('title',xcode(title))
                item.set('author',{'name':xcode(author_name),'url':author_url})
                item.set( 'dt_added',dt_added1)
                item.set('text',xcode(comment))
                item.set('forum',response.meta['forum'])
                item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
                item.set('sk',md5(sk))
                yield item.process()
