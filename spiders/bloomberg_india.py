from juicer.utils import *

class BloomBergIndia(JuicerSpider):
    name = "bloomberg_india"
    start_urls = "http://topics.bloomberg.com/india/"

    def parse(self, response):
        hdoc = HTML(response)

        if self.latest_dt is None:
            self.latest_dt = self._latest_dt
        news = hdoc.select_urls(['//td[contains(@style,"vertical")][1]/table[@cellpadding="0"]//div[@id="stories"]//h3//a/@href'],
                                response)
        [(yield Request(new, self.parse_terminal, response)) for new in news]

    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)

        posted_dt = xcode(textify(hdoc.select('//div[@class="entry_wrap"]//span/@epoch')))
        posted_dt = get_datetime(float(re.findall(r'(\d+)\w\w\w',posted_dt)[0]))

        if posted_dt >= self.latest_dt:
            if self.flag:
                self.update_dt(posted_dt)
            item.set('url', response.url)
            title = textify(hdoc.select('//h1[@class="article_title"]//text()')).replace("&amp;","&").encode('UTF-8')
            item.set('title', xcode(title.replace("&gt;",">").replace("&lt;","<").decode("ascii","ignore")))
            item.set('dt_added', posted_dt)
            author = textify(hdoc.select('//div[@class="entry_wrap"]//span[@class="author"]'))
            author = "".join(re.findall(r'By\s(.*)', author))
            item.set('author.name', xcode(author.replace("&amp;","&")))

            text = textify(hdoc.select('//div[@class="entry_content"]//p[not(contains(@class,"cap_preview") and contains(@class,"cap_show"))]//text()')).replace("\n"," ").encode('UTF-8')
            item.set('text', xcode(text.replace("&amp;","&").replace("&gt;",">").replace("&lt;","<").decode('ascii','ignore')))

            """image_urls = []
            image_url = hdoc.select('//div[@id="story_display"]//div[contains(@class,"thumbnail")]//a//img')
            item.set('image_url',
                      image_urls) if [image_urls.append(xcode(textify(i.select('./@src')))) for i in image_url] else "" """

            yield item.process()

