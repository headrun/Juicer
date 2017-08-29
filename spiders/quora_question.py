from juicer.utils import *

class QuoraQuestionSpider(JuicerSpider):
    name = 'quora_question'

    #http://www.quora.com/Matt-Schiavenza/questions
    #@url(["http://www.quora.com/.*/questions[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        question_feed = get_request_url(response) + '/rss'

        question_urls = hdoc.select('//a[@class="number_answers"][contains(text(), "Followers")]/@href')
        for question_url in question_urls:
            yield Request('http://www.quora.com' + textify(question_url), self.parse_questionmember, response)

    #http://www.quora.com/What-are-some-of-the-top-political-risk-firms-in-the-world-besides-Eurasia-Group
    #@url(["http://www.quora.com/.*-.*-.*[^/]*$"])
    def parse_questionmember(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        question_members = hdoc.select('//a[@class="user"]/@href')
        for question_member in question_members:
            get_page('quora_terminal', 'http://www.quora.com' + textify(question_member))
