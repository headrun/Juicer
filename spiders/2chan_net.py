from juicer.utils import *
from dateutil import parser

class Channet(JuicerSpider):
    name = '2chan_net'
    start_urls =['http://www.2chan.net/index2.html']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//tbody//td/a')

        for node in nodes:
            forum_url = textify(node.select('.//@href'))
            forum_name = xcode(textify(node.select('.//text()')))
            forum_id = forum_url.split('/')[-2]
            forum = {'url':forum_url,'name':forum_name,'id':forum_id}
            yield Request(forum_url,self.parse_threads,response,meta={'forum':forum})

    def parse_threads(self,response):
        hdoc = HTML(response)
        forum = response.meta['forum']
        threads = hdoc.select('//a[@class="hsbn"]/@href').extract()
        _url = '/'.join(response.url.split('/')[:-1])

        for _thread in threads:
            if 'http' not in _thread: _thread = _url + '/' + _thread
            yield Request(_thread,self.thread_details,response,meta={'forum':forum})

        nxt_pg =textify(hdoc.select('//td//input[@accesskey="x"]/ancestor::form/@action'))
        if nxt_pg:
            nxt_pg_url = _url + '/' + nxt_pg
            yield Request(nxt_pg_url,self.parse_threads,response,meta={'forum':forum})

    def thread_details(self,response):
        hdoc = HTML(response)
        forum = response.meta['forum']
        try:title = textify(hdoc.select('//div[@class="thre"]/font/b/text()').extract()[0])
        except:title = textify(hdoc.select('//p[@id="hdp"]/span[@id="tit"]/text()'))
        extra_text = hdoc.select('//div[@class="thre"]//input[@type="checkbox"]/following-sibling::font//text()').extract()[0]
        text1 = textify(hdoc.select('//blockquote/text()'))
        text_final = extra_text + ' ' + text1
        author = hdoc.select('//div[@class="thre"]//input[@type="checkbox"]/following-sibling::font//text()').extract()[1]
        id1 = response.url.split('/')[-3]#textify(hdoc.select('//form/input[@type="checkbox"]/@id'))
        thread_id = response.url.split('/')[-1].split('.htm')[-2]#textify(hdoc.select('//form/input[@type="checkbox"]/@name'))
        thread = {'url':response.url,'id':thread_id,'name':title}
        coment_url = response.url + '#' + id1
        date = textify(hdoc.select('//div[@class="thre"]/text()'))
        import pdb;pdb.set_trace()
        date_final = textify(re.findall('\d+/\d+/\d+',date)) + ' ' + textify(re.findall('\d+:\d+:\d+',date))
        date_final = '20' + date_final
        _dt_added = get_timestamp(parse_date(xcode(date_final)) - datetime.timedelta(hours=9))
        item = Item(response)

        if _dt_added > get_current_timestamp()-86398*2:

                item.set('url',coment_url)
                item.set('title',title)
                item.set('dt_added',_dt_added)
                item.set('text',xcode(text_final))
                item.set('author.name',xcode(author))
                item.set('forum',forum)
                item.set('thread',thread)
                #yield item.process()

        _nodes = hdoc.select('//td[@class="rtd"]')

        for _node in _nodes:
            _id = textify(_node.select('.//input/@id'))
            date2 = textify(_node.select('./text()')).split('Name')[-1]
            date_final = textify(re.findall('\d+/\d+/\d+',date2)) + ' ' + textify(re.findall('\d+:\d+:\d+',date2))
            date_final = '20' + textify(date_final)
            dt_added = get_timestamp(parse_date(xcode(date_final)) - datetime.timedelta(hours=9))
            if dt_added < get_current_timestamp()-86400*1:
                continue
            comment_url= response.url + '#' + _id
            author = textify(_node.select('.//font/b//text()')[1])
            text = textify(_node.select('./font/b/text()').extract()[0])+ ' ' + textify(_node.select('.//blockquote//text()'))

            if _dt_added > get_current_timestamp()-86398*2:
                item.set('url',comment_url)
                item.set('title',xcode(title))
                item.set('dt_added',dt_added)
                item.set('author.name',xcode(author))
                item.set('text',xcode(text))
                item.set('forum',forum)
                item.set('thread',thread)
                #yield item.process()

