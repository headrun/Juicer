from juicer.utils import *

class Quora(JuicerSpider):
    name = "quora"
    start_urls = ['http://www.quora.com/Photoshop-CS6/all_questions', 'http://www.quora.com/Adobe-Photoshop/all_questions']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="PagedList TopicAllQuestionsList"]//div[@class="pagedlist_item"]//div[@class="QuestionText"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_next,response)  
    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="AnswerPagedList PagedList"]//div[@class="ContentFooter AnswerFooter"]//a[@class="answer_permalink"]//@href')
        for url in urls:
            yield Request(url,self.parse_data,response)
    def parse_data(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="header"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="Answer AnswerStandalone"]//div[contains(@id, "container")]//text()'))
        dt_added = textify(hdoc.select('//div[@class="ContentFooter AnswerFooter"]//span//a//text()')).replace('Written', '')
        if 'ago' in dt_added:
            dt_added = dt_added.replace('h', 'hours').replace('m', 'minutes')
        dt_added = parse_date(dt_added)
        if dt_added.date() > get_datetime(get_current_timestamp()).date():
            dt_added = dt_added - datetime.timedelta(days=7)

        dt_added = dt_added - datetime.timedelta(hours=5, minutes=30)
        dt_added = get_timestamp(dt_added)
        author =textify(hdoc.select('//div[@class="Answer AnswerStandalone"]//div[@class="author_info"]//span[@class="feed_item_answer_user"]//span//a[@class="user"]//text()'))
        item = Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set("dt_added",dt_added)
        item.set("author.name",author)
        item.set("url", response.url)
        item.set("xtags", ['quora_sourcetype_manual'])
        yield item.process()
