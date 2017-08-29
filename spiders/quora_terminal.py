from juicer.utils import *

class QuoraTerminalSpider(JuicerSpider):
    name = 'quora_terminal'

    #http://www.quora.com/Matt-Schiavenza
    #@url(["http://www.quora.com/[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        other_links = hdoc.select('//a[@class="sn_icon"]/@href')
        other_links = [textify(o) for o in other_links]
        item.set('other_links', other_links)

        feed_url = get_request_url(response) + '/rss'
        item.set('feed_url', feed_url)

        about_link = get_request_url(response) + '/about'
        yield Request(about_link, self.parse_about, response, meta={'item':item})

        follower_link = get_request_url(response) + '/followers'
        get_page('quora_follower', follower_link)

        following_link = get_request_url(response) + '/following'
        get_page('quora_following', following_link)

        topic_link = get_request_url(response) + '/topics'
        get_page('quora_topic', topic_link)

        board_link = get_request_url(response) + '/boards'
        get_page('quora_board', board_link)

        question_link = get_request_url(response) + '/questions'
        get_page('quora_question', question_link)

        answer_link = get_request_url(response) + '/answers'
        get_page('quora_answer', answer_link)

    #http://www.quora.com/Matt-Schiavenza/about
    #@url(["http://www.quora.com/.*/about[^/]*$"])
    def parse_about(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        got_page(self.name, response)

        sk = get_request_url(response).split('.com/')[-1].split('/')[0]
        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//h1[@class="profile_name_sig"]//a/text()')))
        item.set('title', title)

        stats = {}
        key = hdoc.select('//a[@class="link_label"]/text()')
        key = [textify(k) for k in key]
        value = hdoc.select('//a[@class="link_label"]//span/text()')
        value = [int(textify(v)) for v in value]
        stats = dict(zip(key, value))
        item.set('stats', stats)

        image_url = textify(hdoc.select('//div[@class="profile_photo"]//img/@src'))
        item.set('image_url', image_url)

        description = textify(hdoc.select('//div[@class="inline expanded_q_text"]//div/text()'))
        item.set('description', description)

        location_cities = hdoc.select('//strong[contains(text(), "Location")]//ancestor::div[@class="col w1 p1"]//parent::div[@class="row row_border"]//span[@class="name_text"]//span')
        location_cities = [textify(l) for l in location_cities]
        if location_cities:
            item.set('location_cities', location_cities)

        employment = hdoc.select('//strong[contains(text(), "Employment")]//ancestor::div[@class="col w1 p1"]//parent::div[@class="row row_border"]//span[@class="name_text"]//span')
        employment = [textify(e) for e in employment]
        if employment:
            item.set('employment', employment)

        education = hdoc.select('//strong[contains(text(), "Education")]//ancestor::div[@class="col w1 p1"]//parent::div[@class="row row_border"]//span[@class="name_text"]//span')
        education = [textify(d) for d in education]
        if education:
            item.set('education', education)

        yield item.process()
