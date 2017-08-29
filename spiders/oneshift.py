from juicer.utils import *

class Oneshift(JuicerSpider):
    name = 'oneshift'
    start_urls = ['http://www.oneshift.com/forum/list_topics.php?fid=1','http://www.oneshift.com/forum/list_topics.php?fid=31','http://www.oneshift.com/forum/list_topics.php?fid=6','http://www.oneshift.com/forum/list_topics.php?fid=7']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//tr//td[@class="fmSubText"]')
        for node in nodes:
            date = textify(node.select('./a/text()'))
            if 'by' in date:date = date.split('by')[0]
            else:date = ''
            date_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:continue
            link = textify(node.select('./a/@href'))
            if 'http' not in link:link = 'http://www.oneshift.com/forum/' + link
            yield Request(link,self.details,response)

        nxt_pg = hdoc.select('//span[@class="fmText"]/a[contains(text(),"Next")]/@href').extract()
        if nxt_pg:
            if 'http' not in nxt_pg:nxt_pg = 'http://www.oneshift.com' + nxt_pg[0]
            else:nxt_pg = nxt_pg[0]
            yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//h1[@class="pageTitle"]//text()'))
        forum_title = textify(hdoc.select('//span[@itemtype][last()]/a//text()'))
        forum_url = textify(hdoc.select('//span[@itemtype][last()]/a/@href'))
        if 'http' not in forum_url:forum_url = 'http://www.oneshift.com/forum/' + forum_url
        forum_id = forum_url.split('fid=')[-1]
        thread_id = response.url.split('tid=')[-1].split('&page_id')[0]
        threads = hdoc.select('//tr[@bgcolor]')
        for thread in threads:
            dt = textify(thread.select('.//font[@class="fmText"]/text()')).strip('Posted on:')
            dt_added = get_timestamp(parse_date(xcode(dt))-datetime.timedelta(hours=8))
            author_url = textify(thread.select('.//a[contains(@href,"members/profile.php?userid")][last()]/@href'))
            if 'http' not in author_url:author_url = 'http://www.oneshift.com/' + author_url.strip('.')
            author_name = textify(thread.select('.//a[contains(@href,"members/profile.php?userid")]/b//text()'))
            auth_info = thread.select('.//a[contains(@href,"members/profile.php?userid")]/parent::td//text()').extract()
            comment_url = textify(thread.select('.//a[@class="fmMsgTab"]/@href'))
            comment_id = comment_url.split('msgid=')[-1].split('&fid')[0]
            author_info = []
            for auth in auth_info:
                if str(auth.strip(' ')) == '':continue
                author_info.append(str(auth.strip(' ')))
            text = textify(thread.select('.//td[@class="fmMessage"]/div//text()'))
            text_repl = textify(thread.select('.//td[@class="fmMessage"]/div//script[@type="text/javascript"]//text()'))
            text = text.replace(text_repl,'')
            if text == '':continue
            sk = comment_url
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            item = Item(response)
            item.set('url',response.url + '#' + str(comment_id))
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('author',{'name':xcode(author_name),'url':author_url,'info':author_info})
            item.set('forum',{'title':forum_title,'url':forum_url,'id':forum_id})
            item.set('thread',{'title':xcode(title),'url':response.url,'id':thread_id})
            item.set('text',xcode(text))
            item.set('sk',md5(sk))

        next_pg = hdoc.select('//span[@class="gPages"]/a[contains(text(),"Prev")]/@href').extract()
        if next_pg:
            if 'http' not in next_pg: next_pg = 'http://www.oneshift.com' + next_pg[0]
            else: next_pg = next_pg[0]
            yield Request(next_pg, self.details, response)
