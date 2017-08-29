from juicer.utils import *

class GooglePlusTerminalSpider(JuicerSpider):
    name = 'googleplus_terminal'
    start_urls = ['https://plus.google.com/100000772955143706751/posts']

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('.com/')[-1]
        if '/post' in sk:
            sk = get_request_url(response).split('.com/')[-1].split('/')[0]
            item.set('sk', sk)
        else:
            item.set('sk', sk)

        title = xcode(textify(hdoc.select('//span[@class="fn"]')))
        item.set('title', title)

        image_url = textify(hdoc.select('//div[@class="k-Va-pc-N-A"]//img[@class="kM5Oeb-wsYqfb photo"]/@src'))
        image_url = 'http:' + image_url
        item.set('image_url', image_url)

        sub_title = xcode(textify(hdoc.select('//span[@class="rPciVd"]')))
        item.set('sub_title', sub_title)
        item.textify('sub_title', '//span[@class="rPciVd"]')

        in_circle_count = textify(hdoc.select('//h4[@class="nPQ0Mb c-wa-Da"]')).split('(')[-1].split(')')[0]
        if in_circle_count:
            item.set('in_circle_count', int(in_circle_count))

        have_in_circle_count = textify(hdoc.select('//h4[@class="nPQ0Mb pD8zNd"]')).split('(')[-1].split(')')[0]
        if have_in_circle_count:
            item.set('have_in_circle_count', int(have_in_circle_count))

        in_circle_url = hdoc.select('//h4[not(contains(text(), "Have"))]//parent::div//div[@class="B9veBd"]//div//a/@href')
        in_circle_url = ['https://plus.google.com' + textify(i) for i in in_circle_url]
        item.set('in_circle_url', in_circle_url)
        for url in in_circle_url:
            get_page('googleplus_terminal', url)

        having_in_circle_url = hdoc.select('//h4[contains(text(), "Have")]//parent::div//div[@class="B9veBd"]//div//a/@href')
        having_in_circle_url = ['https://plus.google.com' + textify(h) for h in having_in_circle_url]
        item.set('having_in_circle_url', having_in_circle_url)
        for url in having_in_circle_url:
            get_page('googleplus_terminal', url)

        posts_link = hdoc.select('//span[@class="fD7nue qWSm4c"]//a/@href')
        for url in posts_link:
            url = 'https://plus.google.com/' + textify(url)
            get_page('googleplus_posts', url)

        about_url = (response.url).split('/post')[0]
        about_url = about_url + '/about'
        yield Request(about_url, self.parse_about, response, meta={'item':item})

        plusone_url = (response.url).split('/post')[0]
        plusone_url = plusone_url + '/plusones'
        yield Request(plusone_url, self.parse_plusone, response, meta={'item':item})

    def parse_about(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')

        details = {}
        nodelist = hdoc.select('//div[@class="sNcs4c"]//div[contains(@class, "kM5Oeb")]')
        for node in nodelist:
            key = textify(node.select('.//h2[@class="Wfskpc c-wa-Da"]'))
            value = textify(node.select('.//div[contains(@class, "aYm0te")]'))
            details[key] = value
        item.set('details', details)

        other_links = {}
        key = hdoc.select('//div[@class="dcQzjb C"]//a')
        key = [textify(k).replace('.', '_') for k in key]
        value = hdoc.select('//div[@class="dcQzjb C"]//a/@href')
        value = [textify(v).strip() for v in value]
        other_links = dict(zip(key, value))
        print "other_links>>>>>>>>", other_links
        item.set('other_links', other_links)

        yield item.process()

    def parse_plusone(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')

        plusone_links = hdoc.select('//div[@class="szQdFe kM5Oeb-eETZzf"]//a[@class="g8TxI"]/@href')
        plusone_links = [textify(o) for o in plusone_links]
        item.set('plusone_links', plusone_links)

        yield item.process()
