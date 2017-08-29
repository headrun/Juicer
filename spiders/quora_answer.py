from juicer.utils import *

class QuoraAnswerSpider(JuicerSpider):
    name = 'quora_answer'

    #http://www.quora.com/Matt-Schiavenza/answers
    #@url(["http://www.quora.com/.*/answers[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        answer_feed = get_request_url(response) + '/rss'

        answer_urls = hdoc.select('//a[@class="question_link"]/@href')
        for answer_url in answer_urls:
            yield Request('http://www.quora.com' + textify(answer_url), self.parse_answerlink, response)

    #http://www.quora.com/Travel-Tourism-in-China/What-should-an-American-know-before-going-to-Beijing
    #@url(["http://www.quora.com/.*/[^/]*$"])
    def parse_answerlink(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        answer_members = hdoc.select('//a[@class="user"]/@href')
        for answer_member in answer_members:
            get_page('quora_terminal', 'http://www.quora.com' + textify(answer_member))
