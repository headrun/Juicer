from juicer.utils import *

class Kaskus(JuicerSpider):
    name = 'kaskus'
    start_urls = ['http://www.kaskus.co.id/search/forum?q=toyota&sort=last_post&order=desc']

    def parse(self, response):
        hdoc = HTML(response)
        threads = hdoc.select('//div[@class="listing-table"]//tr[contains(@id,"thread")]')
        for thread in threads:
            post_date = textify(thread.select('.//time/text()'))
            post_date = get_timestamp(parse_date(post_date) - datetime.timedelta(hours=8))
            if post_date < get_current_timestamp()-86400*30:
                continue
            next_page = hdoc.select('//a[@class="next-page"]/@href')
            thread_url = textify(thread.select('.//div[@class="post-title"]/a/@href'))
            thread_url = thread_url + '100000'
            yield Request(thread_url, self.parse_terminal_nfp, response)

        next_page = hdoc.select('//a[@data-original-title="Next Page"]/@href')
        if next_page:
            yield Request(next_page, self.parse, response)

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)
        is_next = True
        forum_base = hdoc.select('//div[@itemprop="breadcrumb"]/a')[-1]

        forum_url = textify(forum_base.select('./@href'))
        forum_id = ''.join(re.findall(r'/\w+/(\w+)/', forum_url))
        forum_title = textify(forum_base.select('./text()'))
        if not forum_url.startswith("http"): forum_url = urlparse.urljoin(response.url, forum_url)

        thread_id = ''.join(re.findall(r'/thread/(\w+)', response.url))
        thread_title = textify(hdoc.select('//div[@class="current"]/text()'))
        if not thread_title:
            thread_title = textify(hdoc.select('//div[@class="breadcrumbs"]/text()'))

        prev_url = ''


        posts = hdoc.select('//div[contains(@class, "postlist")] | //div[contains(@class, "nor-post")]')

        for post in posts:
            post_date = textify(post.select('.//time[@class="entry-date"]/text()'))
            if not post_date:
                continue

            post_date = get_timestamp(parse_date(post_date) - datetime.timedelta(hours=8))
            if post_date < get_current_timestamp()-86400*30:
                is_next = False
                continue

            text = textify(post.select('.//div[@class="entry"]//text()'))
            if not text:
                continue

            url = textify(post.select('.//div[@class="permalink"]/a/@href'))
            if not url.startswith("http"): url = urlparse.urljoin(response.url, url)
            author = textify(post.select('.//div[@class="user-details"]/div[@class="user-name"]/a/text()'))
            author_url = textify(post.select('.//div[@class="user-details"]/div[@class="user-name"]/a/@href'))
            if not author_url.startswith("http"): author_url = urlparse.urljoin(response.url, author_url)
            author_date = textify(post.select('.//div[@class="meta"]/span//text()'))
            posts = textify(post.select('.//div[@class="meta"]/a//text()'))
            auth_title = textify(post.select('.//div[@class="title"]//text()'))
            author = {'name':author,'url':author_url,'title':auth_title,'join':author_date,'posts':posts}
            sk = textify(post.select('.//div[@class="permalink"]/a/@id'))
            sk = ''.join(re.findall(r'postcount(\w+)', sk))
            if not sk:
                continue

            item = Item(response)

            item.set("sk", sk)
            item.set("title", thread_title)
            item.set("text", text)
            item.set("dt_added",post_date)
            item.set("url", url)
            item.set('author',author)

            item.set("forum.id", forum_id)
            item.set("forum.url", forum_url)
            item.set("forum.title", forum_title)

            item.set("thread.id", thread_id)
            item.set("thread.url", response.url)
            item.set("thread.title", thread_title)
            yield item.process()

        last_page = hdoc.select('//a[@class="tooltips last-page"]/@href').extract()
        if last_page:
            if 'http' not in last_page:
                url = 'http://www.kaskus.co.id'+last_page[0]
                yield Request(url, self.parse_terminal_nfp, response)

        prev_url = hdoc.select('//a[@class="tooltips previous-page"]/@href').extract()
        if prev_url and is_next:
            if 'http:' not in prev_url:
                url = 'http://www.kaskus.co.id'+prev_url[0]
                yield Request(url, self.parse_terminal_nfp, response)
