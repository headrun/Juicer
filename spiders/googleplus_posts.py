from juicer.utils import *

class GooglePlusPostsSpider(JuicerSpider):
    name = 'googleplus_posts'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        user_id = get_request_url(response).split('/')[3]
        post_id = get_request_url(response).split('/')[-1]

        sk = post_id + '---' + user_id
        item.set('sk', sk)

        posted_time = textify(hdoc.select('//span[@class="fD7nue qWSm4c"]//a')).split(': ')[-1]
        posted_time = parse_date(posted_time)
        item.set('posted_time', posted_time)

        post_link = textify(hdoc.select('//div[@class="s-r-za"]//a/@href'))
        if post_link:
            item.set('post_link', post_link)

        post_link_description = textify(hdoc.select('//div[@class="s-r-Ge-ec"]'))
        if post_link_description:
            item.set('post_link_description', post_link_description)

        sharing_details = textify(hdoc.select('//span[@title="Sharing details"]'))
        item.set('sharing_details', sharing_details)

        post_head = textify(hdoc.select('//div[@class="rXnUBd"]/text()'))
        item.set('post_head', post_head)

        post_image_url = textify(hdoc.select('//div[@class="s-r-fa"]//div//img/@src'))
        post_image_url = 'http:' + post_image_url
        item.set('post_image_url', post_image_url)

        tagged_persons = hdoc.select('//span[@class="yQteKd"]//a')
        tagged_persons = [textify(p) for p in tagged_persons]
        item.set('tagged_persons', tagged_persons)

        tagged_person_url = hdoc.select('//span[@class="yQteKd"]//a/@href')
        tagged_person_url = ['https://plus.google.com' + textify(t).split('.')[-1] for t in tagged_person_url ]
        #item.set('tagged_person_url', tagged_person_url)
        for url in tagged_person_url:
            get_page('googleplus_terminal', url)

        shares_count = textify(hdoc.select('//div[@class="LwSBrb Ao"]//span[@class="c-C FdmHNd"]')).split(' ')[0]
        item.set('shares_count', int(shares_count))

        commented_person_count = textify(hdoc.select('//span[@class="aISsjb Cs"]'))
        item.set('commented_person_count', int(commented_person_count))

        commented_person_url = hdoc.select('//div[@class="We"]//article//a/@href')
        commented_person_url = ['https://plus.google.com' + textify(p).split('.')[-1] for p in commented_person_url]
        #item.set('commented_person_url', commented_person_url)
        for url in commented_person_url:
            get_page('googleplus_terminal', url)

        comments = []
        person = hdoc.select('//div[@class="We"]//article//a/text()')
        person = [textify(p) for p in person]
        person_comment = hdoc.select('//div[@class="We"]//span[@class="kH"]')
        person_comment = [textify(c) for c in person_comment]
        comments = zip(person, person_comment)
        item.set('comments', comments)

        yield item.process()
