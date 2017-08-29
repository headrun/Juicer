from juicer.utils import *

class EhowSpider(JuicerSpider):
    name = 'ehow_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('_')[-2]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="articleTitle Heading1"]')
        video_url = hdoc.select('//div[@id="PrimaryContent"]//div[@id="VideoData"]/@data-video-hd-id')
        if video_url:
            item.set('video_url', video_url)
            item.textify('video_transcript', '//aside[@id="Transcript"]/blockquote')
        else:
            description = xcode(textify(hdoc.select('//p[@class="intro"]')))
            item.set('description', description)
            item.textify('instructions', '//div[@itemprop="step"]/p')
            item.textify('difficulty', '//dl[@class="difficulty"]//dd')
            resources = hdoc.select('//section[@class="Module resources"]//li')
            resources = [ textify(r) for r in resources ]
            item.set('resources', resources)
        item.textify('image_url', '//figure[@class="Thumbnail articlePhoto"]//a//img/@src')
        yield item.process()
