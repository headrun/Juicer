from juicer.utils import *

class JsonExample(JuicerSpider):
    name = 'json_example'
    start_urls = ['https://latino.bigstar.tv/mobile/movies/genre/all-movies/page/1/limit/30/os/web/device/25eb8e4a7cf5ddfe9c5673e0fbc80ef5/lan/es']

    def parse(self,response):
        json_data = json.loads(response.body)
        movies_list = json_data['films']
        for movie in movies_list:
            import pdb;pdb.set_trace()
            movie_id = movie['id']
            movie_duration = movie['duration']
            movie_genre = movie['genre']
            movie_link =movie['shareLink']
