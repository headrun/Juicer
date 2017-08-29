from generic_browse import Spider as GenericBrowseSpider

class Spider(GenericBrowseSpider):
    name = 'generic_browse_recent'
    run_type = 'recent'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
