from juicer.utils import *

def fill_all_electronics(hdoc):
    #fill up all info for item
    #extract all info, store in a dictionary called data
    #return data
    data = {}
    data['company'] = textify(hdoc.select('//div[@class="buying"]//span//a/text()'))
    data['listing_price'] = textify(hdoc.select('//td//span[@class="listprice"]/text()')).replace('$','')
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$','')
    data['discount'] = textify(hdoc.select('//td[@class="price"]/text()')).strip().split(' ')[-1].replace('(','').replace(')','')
    data['availability'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['description'] = textify(hdoc.select('//h3[@class][contains(text(),"Product Description")]//following-sibling::div[@class="productDescriptionWrapper"]//text()'))
    data['tech_details'] = textify(hdoc.select('//h2[contains(text(),"Technical Details")]//following-sibling::div[@class="content"]//ul//li/text()'))
    data['product_details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    return data
    item.set('data', data)

def fill_computer_accessories(hdoc):
    data = {}
    data['company'] = textify(hdoc.select('//div[@class="buying"]//span//a/text()'))
    data['listing_price'] = textify(hdoc.select('//span[@class="listprice"]/text()')).replace('$','')
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$','')
    data['discount'] = textify(hdoc.select('//td[@class="price"]/text()')).strip().split(' ')[-1].replace('(','').replace(')','')
    data['availability'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['description'] = textify(hdoc.select('//h3[@class][contains(text(),"Product Description")]//following-sibling::div[@class="productDescriptionWrapper"]//text()'))
    data['tech_details'] = textify(hdoc.select('//h2[contains(text(),"Technical Details")]//following-sibling::div[@class="content"]//ul//li/text()'))
    data['product_details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    return data
    item.set('data', data)

def fill_movies_tv(hdoc):
    data = {}
    data['crew'] = textify(hdoc.select('//div[@class="subTitle"]//a/text()'))
    data['listing_price'] = textify(hdoc.select('//td[text()="List Price:"]//following-sibling::td//span[@class]/text()')).replace('$','')
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$','')
    data['discount'] = textify(hdoc.select('//td[@class="price"]/text()')).strip().split(' ')[-1].replace('(','').replace(')','')
    data['availability'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['description'] = textify(hdoc.select('//div[@class="productDescriptionWrapper"]/text()'))
    data['features'] = textify(hdoc.select('//h2[contains(text(),"Special Features")]//following-sibling::div[@class="content"]//ul//li/text()'))
    data['product_details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    data['format'] = textify(hdoc.select('//div[@class="subTitle"]/text()')).strip().split('\n\n\n')[-1]
    data['rated'] = textify(hdoc.slect('//div[@class="subTitle"]/text()')).strip().split('\n\n\n')[-3]
    return data
    item.set('data', data)

def fill_music(hdoc):
    data = {}
    data['artist'] = textify(hdoc.select('//div[@class="buying"]//span//a/text()'))
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$','')
    data['availability'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['editorial_reviews'] = textify(hdoc.select('//div[@class="productDescriptionWrapper"]/text()'))
    data['product_details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    data['music_type'] = textify(hdoc.select('//span[@id="btAsinTitle"]//span/text()'))
    return data
    item.set('data', data)

def fill_musical_instruments(hdoc):
    data = {}
    data['company'] = textify(hdoc.select('//div[@class="buying"]//span//a/text()'))
    data['listing_price'] = textify(hdoc.select('//td//span[@class="listprice"]/text()')).replace('$','')
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$','')
    data['discount'] = textify(hdoc.select('//td[@class="price"]/text()')).strip().split(' ')[-1].replace('(','').replace(')','')
    data['availability'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['description'] = textify(hdoc.select('//h3[@ class="productDescriptionSource"]//following-sibling::div[@class="productDescriptionWrapper"]//text()'))
    data['features'] = textify(hdoc.select('//h2[contains(text(),"Product Features")]//following-sibling::div[@class="content"]//ul//li/text()'))
    data['product_details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    return data
    item.set('data', data)

def fill_books(hdoc):
    data = {}
    data['author'] = textify(hdoc.select('//span[@class="contributorNameTrigger"]//a[1]/text()'))
    data['list_price'] = textify(hdoc.select('//span[@class="listprice"]/text()')).replace('$','')
    data['price'] = textify(hdoc.select('//b[@class="priceLarge"]/text()')).replace('$',' ')
    data['discount'] = textify(hdoc.select('//tr[@class="youSavePriceRow"]//td[@class="price"]/text()')).strip().split(' ')[-1].replace('(','').replace(')','')
    data['availabilty'] = textify(hdoc.select('//span[@class="availGreen"]/text()'))
    data['description'] = textify(hdoc.select('//h3[@class][contains(text(),"Product Description")]//following-sibling::div[@class="productDescriptionWrapper"]//text()'))
    data['editorial_reviews'] = textify(hdoc.select('//div[@class="productDescriptionWrapper"]//a//strong//..//following-sibling::text()'))
    data['details'] = textify(hdoc.select('//td[@class="bucket"]//div[@class="content"]//ul//li/b/text()'))
    data['book_type'] = textify(hdoc.select('//span[@id="btAsinTitle"]//span/text()'))
    return data
    item.set('data', data)


#Dictionary that contains pointers to all the functions above
#note: the keys are the text category extracted from 'get_category' function
#finds the category on the site
#update this dictionary along with functions as more categories are discovered

CALL_FOR_CATEGORY = {'All Electronics':fill_all_electronics,
                     'Computer & Accessories': fill_computer_accessories,
                     'Movies & TV': fill_movies_tv,
                     'Music': fill_music,
                     'Musical Instruments': fill_musical_instruments,
                     'Books': fill_books}

def gen_start_urls():
    items = lookup_items('amazon_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

def get_sk(url):
    """
    gets the sk for a url
    """

    split_url = url.split('/')
    sk = None

    if '/product/' in url:
        sk = split_url[split_url.index('product') + 1]
    elif '/dp/' in url:
        sk = split_url[split_url.index('dp') + 1]
    elif '/product-reviews/' in url:
        sk = split_url[split_url.index('product-reviews') + 1]

    return sk

def fill_basic_info(item, hdoc):
    """
    Fills the basic info for any item (given a terminal page hdoc)
    """

    img_url = textify(hdoc.select('//form[@id="handleBuy"]'\
                                  '/table[@class="productImageGrid"]'\
                                  '//img[@id="main-image" or'\
                                  '@id="prodImage"]/@src'))
    if not img_url:
        img_url = textify(hdoc.select('//form[@id="handleBuy"]'\
                                      '/table[@class="productImageGrid"]'\
                                      '//div[@class="centerslate"]'\
                                      '//img/@src'))
    else:
        img_url = ''

    #TODO : Implement image url for all types on the site, so far couldn find anything common
    #http://www.amazon.com/Kindle-Wireless-Reading-Display-Generation/dp/B002GYWHSQ/ref=sa_menu_kdx23/180-6407114-1468658

    title = textify(hdoc.select('//span[@id="btAsinTitle"]/text()'))

    rating = textify(hdoc.select('//form[@id="handleBuy"]'\
                                 '//span[@class="asinReviewsSummary"]'\
                                 '/a/span/@title'))

    num_reviews = textify(hdoc.select('//form[@id="handleBuy"]'\
                                      '//span[@class="crAvgStars"]'\
                                      '/a/text()'))

    amazon_likes = textify(hdoc.select('//span[@class="amazonLikeCount"]/text()'))

    rating = float(rating.split()[0]) if rating else None
    num_reviews = int(''.join(num_reviews.split()[0].split(','))) if num_reviews else None

    item.set('title', title)
    item.set('img_url', img_url)
    item.set('rating', rating)
    item.set('num_reviews', num_reviews)
    item.set('amazon_likes',amazon_likes)


def get_category(hdoc):
    """
    Finds the category of a product, given the terminal page
    """

    category = textify(hdoc.select('//div[@class="navCatSpc"]/a/text()'))
    return category


class AmazonTerminalSpider(JuicerSpider):
    name = 'amazon_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        #we know all urls we get point to terminal pages
        item = Item(response, HTML)
        #fill basic details
        fill_basic_info(item, hdoc)
        url = response.url
        sk = get_sk(url)

        if not sk:
            return

        #print '*'*150

        item.set('sk', sk)
        #according to the category it goes to a different function
        #for each category, the data extraction technique is different, hence this process
        category = get_category(hdoc)

        #For every function that is written per category, return a dictionary of all the data extracted
        #if result is {} , it means that category does not exist in dictionary hence empty dictionary
        extended_data = CALL_FOR_CATEGORY.get(category, lambda hdoc: {})(hdoc)
        item.set('extended_data', extended_data)

        item.set('category', category)
        item.set('got_page', True)
        item.set('url', response.url)
        item.update_mode = 'custom'

        #Reviews
        review_url = textify(hdoc.select('//form[@id="handleBuy"]//span[@class="crAvgStars"]/a/@href'))
        if review_url:
            item.set('review_url', review_url)

        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        if item.has_key('review_url'):
            got_review_page = item.get('got_review_page', False)
            return [('got_page:%s' % got_page, item['url']), ('got_review_page:%s' %got_review_page, item['review_url'])]
        else:
            return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = AmazonTerminalSpider()
