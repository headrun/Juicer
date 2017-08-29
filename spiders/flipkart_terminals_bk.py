from juicer.utils import *

class FlipkartTerminals(JuicerSpider):
    name = 'flipkart_terminals1'

    def parse(self, response):
        got_page(self.name, response)
        hdoc = HTML(response)

        next_page = ''
        posts = hdoc.select('//div[@class="review-list"]/div')
        for post in posts:
            item = Item(response)
            post_dt = textify(post.select('.//div[contains(@class,"date")]'))
            post_dt = parse_date(post_dt, True)
            title = textify(post.select('.//div[contains(@class,"fk-font-normal")]/strong'))
            text = textify(post.select('.//p[contains(@class,"margin")]'))
            url = textify(post.select('.//a[contains(text(), "Permalink")]/@href'))
            url = response.url + '#' + url.split('/')[-1]
            author = textify(post.select('.//div[@class="line"]/span|.//div[@class="line"]/a'))
            auth_url = textify(post.select('.//div[@class="line"]/a/@href'))
            rating = textify(post.select('.//div[@class="fk-stars"]/@title'))
            rating = ''.join(re.findall(r'\d+', rating))
            url = urlparse.urljoin(response.url, url)
            category = textify(hdoc.select('//h1/a/text()'))
            next_page = textify(hdoc.select('//div[contains(@class,"navigation")]\
                        /a[contains(text(), "Next")]/@href'))

            item.set('author.name', author)
            item.set('author.url', auth_url) if auth_url else ''
            item.set('category', category)
            item.set('title', title)
            item.set('dt_added', post_dt)
            item.set('text', text)
            item.set('url', url)
            item.set('num.rating', int(rating)) if rating else ''
            ob = pprint.PrettyPrinter(indent=2)
            ob.pprint(item.data)

        if next_page:
            next_page = urlparse.urljoin(response.url, next_page)
            get_page(self.name, next_page)

