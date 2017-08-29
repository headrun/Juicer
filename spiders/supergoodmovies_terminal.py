from juicer.utils import *

class SuperGoodMoviesTerminalSpider(JuicerSpider):
    name = 'supergoodmovies_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('.com/')[1].split('/')[0]
        print "skkkkkkk>>>>>>>>>>>>>>", sk
        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//h1[@class="det_ntitle fs20"]'))).replace("\u2013", "")
        print "title>>>>>>>>>>>>>>>>>>", title
        item.set('title',title)

        updated_time = textify(hdoc.select('//b[contains(text(), "Updated on :")]/following-sibling::text()'))
        print "updated time>>>>>>>>>>>", updated_time
        item.set('updated_time', updated_time)

        views = textify(hdoc.select('//p[contains(text(),"Views:")]/preceding-sibling::p'))
        if views:
            print "views>>>>>>>>>>>>>>", views
            item.set('views', int(views))

        user_rating = textify(hdoc.select('//p[contains(text(),"User Rating:")]/preceding-sibling::p'))
        if user_rating:
            print "user_rating>>>>>>>>>>>>>>>", user_rating
            item.set('user_rating', user_rating)

        image_url = textify(hdoc.select('//p[@class="grid_inner_bigimage"]/img/@src'))
        print "image_url>>>>>>>>>>>>>>", image_url
        item.set('image_url', image_url)

        node = xcode(textify(hdoc.select('//div[@class="deatailspage_news"]//text()'))).replace("\u2013", "")

        if node:
            description = xcode(node.split('Listen Review:')[0]).replace("\u2013", "")
            if description:
                print "description>>>>>>>>>>>>>>>", description
                item.set('description', description)

            if "Story:" in node:
                story = xcode(node.split('Story:')[1].split('Analysis:')[0]).replace("\u2013", "")
                print "story>>>>>>>>>>>>>", story
                item.set('story', story)

            if "Analysis:" in node:
                analysis = xcode(node.split('Analysis:')[1].split('Performances:')[0]).replace("\u2013", "")
                print "analysis>>>>>>>>>>>>>", analysis
                item.set('analysis', analysis)

            if "Performances:" in node:
                performances = xcode(node.split('Performances:')[1].split('Technicalities:')[0]).replace("\u2013", "")
                print "performances>>>>>>>>>>>", performances
                item.set('performances', performances)

            if "Technicalities:" in node:
                techincalities = xcode(node.split('Technicalities:')[1].split('Final Word:')[0]).replace("\u2013", "")
                print "techincalities>>>>>>>>>>>>>", techincalities
                item.set('techincalities', techincalities)

            if "Final Word:" in node:
                final_word = xcode(node.split('Final Word:')[1].split('Movie Rating:')[0]).replace("\u2013", "")
                print "final word>>>>>>>>>>>>>", final_word
                item.set('final_word', final_word)

            movie_rating = textify(hdoc.select('//span[@class="details_text"]//b[contains(text(), "ating")]')).replace("Rating", "").replace("Banner", "").replace(":", "")\
                           or textify(hdoc.select('//span[contains(text(), "ating")]')).replace("Rating", "").replace("Banner", "").replace(":", "")
            if movie_rating:
                print "movierating>>>>>>>>>>>>", movie_rating
                item.set('movie_rating', movie_rating)

            if "Banner:" in node:
                banner = textify(hdoc.select('//b[contains(text(), "Banner:")]/following-sibling::text()[1]'))\
                         or textify(hdoc.select('//span[contains(text(), "Banner:")]/following-sibling::text()[1]'))\
                         or textify(hdoc.select('//span[contains(text(), "Rating")]/following-sibling::text()[1]')).replace("Banner:", "")\
                         or textify(hdoc.select('//span[@class="details_text"]/text()[contains(string(),"Banner")]')).replace("Banner:", "")
                print "banner>>>>>", banner
                item.set('banner',banner)
            if "Cast" in node:
                cast = textify(hdoc.select('//b[contains(text(), "Cast")]/following-sibling::text()[1]')).replace(":", "")\
                        or textify(hdoc.select('//span[@class="details_text"]//span[contains(text(), "Cast")]//following-sibling::a/text()[1]'))\
                        or textify(hdoc.select('//span[contains(text(), "Cast")]/following-sibling::text()[1]')).replace(":", "")\
                        or list(set(textify(hdoc.select('//span[@class="details_text"]//a[contains(@href, "-Gallery")]/text()')).split(",")))
                print "cast>>>>>>>>>>>>>", cast
                item.set('cast',cast)
            if "Music"in node: 
                music = textify(hdoc.select('//b[contains(text(), "Music")]/following-sibling::text()[1]')).replace(":", "")\
                        or textify(hdoc.select('//span[contains(text(), "Music")]/following-sibling::text()[1]')).replace(":", "")\
                        or textify(hdoc.select('//span[@class="details_text"]/text()[contains(string(),"Music")]')).replace("Music:",     "")
                print "music>>>>>>>>>>>>>>", music
                item.set('music',music)
            if "Direct" in node:
                director = textify(hdoc.select('//b[contains(text(), "Direct")]/following-sibling::text()[1]')).replace(":", "")\
                           or textify(hdoc.select('//span[contains(text(), "Direct")]/following-sibling::text()[1]')).replace(":", "")\
                           or textify(hdoc.select('//span[@class="details_text"]/text()[contains(string(),"Direct")]')).replace("Director:","")
                print "director>>>>>>>>>>>>>>", director
                item.set('director', director)
            if "Producer" in node:
                producer = textify(hdoc.select('//b[contains(text(), "Producer")]/following-sibling::text()[1]')).replace(":", "")\
                           or textify(hdoc.select('//span[contains(text(), "Producer")]/following-sibling::text()[1]')).replace(":", "") \
                           or textify(hdoc.select('//span[@class="details_text"]/text()[contains(string(),"Producer")]')).replace("Producer:",         "")
                print "producer>>>>>>>>>>>>>>",producer 
                item.set('producer', producer)

        #yield item.process()
