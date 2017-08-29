from juicer.utils import *

class QuoraTopicSpider(JuicerSpider):
    name = 'quora_topic'

    #http://www.quora.com/Matt-Schiavenza/topics
    #@url(["http://www.quora.com/.*/topics[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        topics_urls = hdoc.select('//div[@class="light feed_item_activity"]//a[contains(text(), "Answers")]/@href')
        for topics_url in topics_urls:
            yield Request('http://www.quora.com' + textify(topics_url), self.parse_topiclinks, response)

    #http://www.quora.com/Matt-Schiavenza/answers/China
    #@url(["http://www.quora.com/.*/answers/.*[^/]*$"])
    def parse_topiclinks(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        topics = hdoc.select('//a[@class="question_link"]/@href')
        for topic in topics:
            yield Request('http://www.quora.com' + textify(topic), self.parse_topicmember, response)

    #http://www.quora.com/International-Politics/Why-did-a-top-Chinese-official-recently-say-that-the-United-States-will-retain-unchallengeable-global-dominance-for-at-least-two-decades
    #@url(["http://www.quora.com/.*/.*-.*-.*[^/]*$"])
    def parse_topicmember(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        topic_memberlinks = hdoc.select('//a[@class="user"]/@href')
        for topic_memberlink in topic_memberlinks:
            get_page('quora_terminal', 'http://www.quora.com' + textify(topic_memberlink))
