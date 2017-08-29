from juicer.utils import *
def gen_start_urls():
    items = lookup_items('cardealerreviews_terminal', 'got_page:False', limit=100)
    for _id, term, data in items:
        yield data

class CardealerreviewsTerminalSpider(JuicerSpider):
    name = 'cardealerreviews_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('p=')[1]
        item.set('sk',sk)
        item.textify('title', '//h1[@class="entry-title"]')
        address = textify(hdoc.select('//table//td[@style="width:50%"][1]'))
        contact = textify(hdoc.select('//table//td[@style="width:50%"][2]'))
        item.set('address', address)
        item.set('contact', contact)
        item.textify('previous post', '//p[@class="previous"]//a')
        item.textify('next post', '//p[contains(text(),"Next post: ")]//following-sibling::a')
        item.textify('revw_count', '//div[@class="comments_intro"]//p//span')
        nodes = hdoc.select('//dl[@id="comment_list"]')
       # Reviews
        reviews = {}
        details = []
        for node in nodes:
            reviewer = textify(node.select('.//span[@class="comment_author"]'))
            revw_updated_at = textify(node.select('.//span[@class="comment_time"]//a'))
            revw_desc = textify(node.select('.//div[@class="format_text"]//p[1]'))
            details.append(reviewer)
            details.append(revw_date)
            details.append(revw_desc)
            reviews = details
        item.set('reviews', reviews)
        item.set('got_page', True)
        item.update_mode = 'custom'
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            return old_data
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = CardealerreviewsTerminalSpider()


