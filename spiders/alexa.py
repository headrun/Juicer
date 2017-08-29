#Written by Jatin Verma on 19/07/2011
import re
import datetime

from juicer.utils import *

class Spider(JuicerSpider):

    name = "alexa"
    start_urls = ['http://www.alexa.com/topsites']

    def parse(self, response):
        count = 0
        hdoc = HTML(response)
        sites_li = hdoc.select('//li[@class="site-listing"]')
        for site_li in sites_li:
            item = Item(response, HTML)
            site_rank = textify(site_li.select('.//div[@class="count"]/text()'))
            site_name = textify(site_li.select('.//div/h2/a[@href]/text()'))
            site_url = textify(site_li.select('.//div/span[@class="small topsites-label"]/text()'))
            site_desc = textify(site_li.select('.//div[@class="description"]/text()'))
            site_desc_more = textify(site_li.select('.//div[@class=description]/span[@class="remainder"]/text()'))
            site_description = site_desc + site_desc_more
            site_star_rating = textify(site_li.select('.//div[@id=""][contains(@class,"stars rating")]/span/text()'))
            site_yield = site_li.select('.//div[@class="desc-container"]/h2/a/@href')
            count = count + 1

            sk = site_url
            item.set('sk', sk )
            item.set('Site Rank', site_rank)
            item.set('Site Name', site_name)
            item.set('Site URL', site_url)
            item.set('Site Description', site_description)
            item.set('Site Star Rating', site_star_rating)

            yield Request(site_yield, self.get_site_info, response, meta={"item":item} )

        next_page = hdoc.select('//a[contains(text(),"Next")]/@href')
        yield Request(next_page, self.parse, response)

    def get_site_info(self, response):

        hdoc = HTML(response)
        item = response.meta.get('item')

        aud_bkdn = {}
        aud_bkdn_Age = hdoc.select('//div[@class="demog_box"]//strong[contains(text(),"Age")]//parent::div//parent::div[@class="demog_box"]//div[@class="demog_percentages"]')
        for div_percentage in aud_bkdn_Age:
            name = textify(div_percentage.select('.//span[@class="demog_label"]/text()'))
            tag_popularity = textify(div_percentage.select('.//span[@class="middle"]/strong[1]'))
            relative = ""
            if "similar" in tag_popularity:
                 relative = "similar"
            elif "over-represented" in tag_popularity:
                relative = "over-represented"
            elif "under-represented" in tag_popularity:
                relative = "under-represented"

            demog_offset = textify(div_percentage.select('.//span[@class="demog_offset"]/@style'))
            offset = demog_offset.split(":")[1]
            offset = offset.replace("px","")
            demog_stat = 50 - float(offset)

            aud_bkdn_age = {'name':name, 'relative_popularity':relative, 'demog_stat':demog_stat}
            aud_bkdn['Age'] = aud_bkdn_age

        aud_bkdn_Edu = hdoc.select('//div[@class="demog_box"]//strong[contains(text(),"Education")]//parent::div//parent::div[@class="demog_box"]//div[@class="demog_percentages"]')
        for div_percentage in aud_bkdn_Age:
            name = textify(div_percentage.select('.//span[@class="demog_label"]/text()'))

            tag_popularity = textify(div_percentage.select('.//span[@class="middle"]/strong[1]'))
            relative = ""
            if "similar" in tag_popularity:
                relative = "similar"
            elif "over-represented" in tag_popularity:
                relative = "over-represented"
            elif "under-represented" in tag_popularity:
                relative = "under-represented"

            demog_offset = textify(div_percentage.select('.//span[@class="demog_offset"]/@style'))
            offset = demog_offset.split(":")[1]
            offset = offset.replace("px","")
            demog_stat = 50 - float(offset)
            aud_bkdn_edu = {'name':name, 'relative popularity':relative, 'demog_stat':demog_stat}
            aud_bkdn['Education'] = aud_bkdn_edu

        aud_bkdn_Gen = hdoc.select('//div[@class="demog_box"]//strong[contains(text(),"Gender")]//parent::div//parent::div[@class="demog_box"]//div[@class    ="demog_percentages"]')
        for div_percentage in aud_bkdn_Gen:
            #to get the name
            name = textify(div_percentage.select('.//span[@class="demog_label"]/text()'))

            #to get the audience popularity relative to internet population
            tag_popularity = textify(div_percentage.select('.//span[@class="middle"]/strong[1]'))
            relative = ""
            if "similar" in tag_popularity:
               relative = "similar"
            elif "over-represented" in tag_popularity:
                relative = "over-represented"
            elif "under-represented" in tag_popularity:
                relative = "under-represented"

            #to get the demog stat
            demog_offset = textify(div_percentage.select('.//span[@class="demog_offset"]/@style'))
            offset = demog_offset.split(":")[1]
            offset = offset.replace("px","")
            demog_stat = 50 - float(offset)

            aud_bkdn_gen = {'name':name, 'relative popularity':relative, 'demog_stat':demog_stat}
            aud_bkdn['Gender'] = aud_bkdn_gen

        aud_bkdn_Chd = hdoc.select('//div[@class="demog_box"]//strong[contains(text(),"Has Children")]//parent::div//parent::div[@class="demog_box"]//div[@class="demog_percentages"]')
        for div_percentage in aud_bkdn_Chd:
            #to get the name
            name = textify(div_percentage.select('.//span[@class="demog_label"]/text()'))
            relative = ""
            #to get the audience popularity relative to internet population
            tag_popularity = textify(div_percentage.select('.//span[@class="middle"]/strong[1]'))
            relative =""
            if "similar" in tag_popularity:
                relative = "similar"
            elif "over-represented" in tag_popularity:
                relative = "over-represented"
            elif "under-represented" in tag_popularity:
                relative = "under-represented"

            #to get the demog stat
            demog_offset = textify(div_percentage.select('.//span[@class="demog_offset"]/@style'))
            offset = demog_offset.split(":")[1]
            offset = offset.replace("px","")
            demog_stat = 50 - float(offset)

            aud_bkdn_chd = {'name':name, 'relative popularity':relative, 'demog_stat':demog_stat}
            aud_bkdn['Children'] = aud_bkdn_chd

        aud_bkdn_BrLoc = hdoc.select('//div[@class="demog_box"]//strong[contains(text(),"Browsing Location")]//parent::div//parent::div[@class="demog_box"]//div[@class="demog_percentages"]')
        for div_percentage in aud_bkdn_BrLoc:
            #to get the name
            name = textify(div_percentage.select('.//span[@class="demog_label"]/text()'))

            #to get the audience popularity relative to internet population
            relative = ""
            tag_popularity = textify(div_percentage.select('.//span[@class="middle"]/strong[1]'))
            if "similar" in tag_popularity:
                relative = "similar"
            elif "over-represented" in tag_popularity:
                relative = "over-represented"
            elif "under-represented" in tag_popularity:
                relative = "under-represented"

            #to get the demog stat
            demog_offset = textify(div_percentage.select('.//span[@class="demog_offset"]/@style'))
            offset = demog_offset.split(":")[1]
            offset = offset.replace("px","")
            demog_stat = 50 - float(offset)

            aud_bkdn_brloc = {'name':name, 'relative popularity':relative, 'demog_stat':demog_stat}
            aud_bkdn['Location'] = aud_bkdn_brloc

            item.set('Audience Demographics', aud_bkdn )

        #Related Links
        rel_links = hdoc.select('//div[@id="relatedlinks-content"]//li')

        lst_rel_links = []

        for li in rel_links:
            rel_link = {}
            #get the number
            number = textify(li.select('.//span[@class="num"]/text()'))
            #number = int(number)
            #get the site
            site = textify(li.select('.//strong/text()'))

            rel_link = {'number':number, 'site':site}
            lst_rel_links.append(rel_link)

        item.set('Relative Links', lst_rel_links )

        #Reviews
        rev_links = hdoc.select('//div[@id="ratingOverview"]//div[@class="alignleft"]/div[@class="rating_percentages"]')
        dict_star_rating = {}
        dict_rev_links = {}
        for rev_link in rev_links:

            star_rating = textify(rev_link.select('.//span[@class="rating_label"]/text()'))
            star_rating_value = textify(rev_link.select('.//span[@class="rating_total"]/text()'))
            star_rating_value = star_rating_value.replace('(','').replace(')','')
            dict_star_rating[star_rating] = star_rating_value

        lst_review = []
        review_lst = hdoc.select('//div[@id="reviewContent"]//div[@class="review"]')
        for review_iter in review_lst:
            best_use = "".join(textify(review_iter.select('.//div[@class="reviewText"]//p')))
            title = textify(review_iter.select('.//ul[@class="titleBar "]//li[@class="title"]'))
            star_rating = textify(review_iter.select('.//div[@id=""]'))
            date = textify(review_iter.select('.//li[@class="date"]'))
            user = textify(review_iter.select('.//div[@class="reviewText"]//a'))
            comments = textify(review_iter.select('.//div[@class="reviewText"]/text()[last()]'))
            #dict_review = {}
            dict_review = {'best_use':best_use, 'title':title, 'star_rating':star_rating, 'date':date, 'user':user, 'comments':comments } 
            #likes =[]
            likes = textify(review_iter.select('.//div[@class="pairs"]/ul/li/text()'))

            lst_review.append(dict_review)
            lst_review.append(likes)

        dict_rev_links['star summary'] = dict_star_rating
        dict_rev_links['review list'] = lst_review

        item.set('Reviews', dict_rev_links )

        #Traffic Stats
        #average load time
        avg_load_time = "".join(textify(hdoc.select('//div[@class="speedAd"]//p[1]//text()')))

        #rank
        description = textify(hdoc.select('//div[@id="rank"]/p[1]/text()'))
        dict_rank = {}
        #timelist
        tm_lst_rank = hdoc.select('//table[@class="rank"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_iter in tm_lst_rank:
            dict_time_rank = {}
            change = textify(tm_lst_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_iter.select('.//th/text()'))
            traffic_rank = textify(tm_lst_iter.select('.//th/text()'))
            dict_time_rank['change'] = change
            dict_time_rank['name'] = name
            dict_time_rank['traffic_rank'] = traffic_rank
            time_lst.append(dict_time_rank)

        dict_rank['desc'] = description
        dict_rank['time_list'] = time_lst

        item.set('Tr_Rank', dict_rank)
        #visitors percent
        dict_visitors = {}
        vst_per_description = textify(hdoc.select('//div[@id="reach"]//p[1]/text()'))
        tm_lst_vst_per = hdoc.select('//table[@class="visitors_percent"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_vst_per_iter in tm_lst_vst_per:
            dict_time_vis = {}
            reach = textify(tm_lst_vst_per_iter.select('.//td[@class="avg "]//text()'))
            change = textify(tm_lst_vst_per_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_vst_per_iter.select('.//th//text()'))
            dict_time_vis['reach']  = reach
            dict_time_vis['change'] = change
            dict_time_vis['name'] = name
            time_lst.append(dict_time_vis)
        dict_visitors['desc'] = vst_per_description
        dict_visitors['time_list'] = time_lst

        item.set('Tr_Visitors_percent',dict_visitors)

        #bounce percent
        dict_bounce = {}
        bounce_per_desc = textify(hdoc.select('//div[@id="bounce"]//p[1]/text()'))
        tm_lst_bounce_per = hdoc.select('//table[@class="bounce_percent"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_bounce_per_iter in tm_lst_bounce_per:
            dict_time_boun = {}
            change = textify(tm_lst_bounce_per_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_bounce_per_iter.select('.//th//text()'))
            bounce_percent = textify(tm_lst_bounce_per_iter.select('.//td[@class="avg "]//text()'))
            dict_time_boun['change'] = change
            dict_time_boun['name'] = name
            dict_time_boun['bounce_percent'] = bounce_percent
            time_lst.append(dict_time_boun)
        dict_bounce['desc'] = bounce_per_desc
        dict_bounce['time_list'] = time_lst

        item.set('Tr_Bounce_percent', dict_bounce)
        #worldwide traffic rank
        pair_lst = hdoc.select('//div[@id="traffic-rank-by-country"]//div[contains(@class, "tr1")]//p//parent::div')
        country_lst = []
        dict_wwtr = {}
        for pair in pair_lst:
            dict_country = {}
            rank = textify(pair.select('.//p[@class="tc1"][@style="width:40%; text-align:right;"]/text()'))
            country_name = textify(pair.select('./p/a/text()[2]'))
            dict_country['rank'] = rank
            dict_country['country_name'] = country_name
            country_lst.append(dict_country)
        dict_wwtr['country_list'] = country_lst
        item.set('Tr_Worldwide_Traffic_rank', dict_wwtr)
        #pageviews percent
        dict_pgper = {}
        page_view_description = textify(hdoc.select('//div[@id="pageviews"]//p//text()'))
        tm_lst_pgvw_per = hdoc.select('//table[@class="pageviews_percent"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_pgvw_per_iter in tm_lst_pgvw_per:
            dict_time = {}
            change = textify(tm_lst_pgvw_per_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_pgvw_per_iter.select('.//th//text()'))
            page_views = textify(tm_lst_pgvw_per_iter.select('.//td[@class="avg "]//text()'))
            dict_time['change'] = change
            dict_time['name'] = name
            dict_time['page_views'] = page_views
            time_lst.append(dict_time)
        dict_pgper['desc'] = page_view_description
        dict_pgper['time list'] = time_lst
        item.set('Tr_pageviews_percent',dict_pgper)
        #pageviews per user/visitor
        dict_pgpvis = {}
        page_view_per_user_description = textify(hdoc.select('//div[@id="pageviews_per_user"]//p//text()'))
        tm_lst_pageview_user = hdoc.select('//table[@class="pageviews_per_visitor"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_pageview_user_iter in tm_lst_pageview_user:
            dict_time = {}
            change = textify(tm_lst_pageview_user_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_pageview_user_iter.select('.//th//text()'))
            page_views_per_user = textify(tm_lst_pageview_user_iter.select('.//td[@class="avg "]//text()'))
            dict_time['change'] = change
            dict_time['name'] = name
            dict_time['page_views_per_user'] = page_views_per_user
            time_lst.append(dict_time)
        dict_pgpvis['desc'] = page_view_per_user_description
        dict_pgpvis['time list'] = time_lst
        item.set('Tr_peruser_pervisitor',dict_pgpvis)
        #time on site
        dict_tos = {}
        tos_description = textify(hdoc.select('//div[@id="time_on_site"]//p//text()'))
        tm_lst_tos = hdoc.select('//table[@class="time_on_site"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_tos_iter in tm_lst_tos:
            dict_time = {}
            change = textify(tm_lst_tos_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_tos_iter.select('.//th//text()'))
            time_on_site = textify(tm_lst_tos_iter.select('.//td[@class="avg "]//text()'))
            dict_time['change'] = change
            dict_time['name'] = name
            dict_time['time_on_site'] = time_on_site
            time_lst.append(dict_time)
        dict_tos['desc'] = tos_description
        dict_tos['time list'] = time_lst
        item.set('Tr_time on site',dict_tos)

        #search percent
        dict_searp = {}
        search_percent_description = textify(hdoc.select('//div[@id="search"]//p//text()'))
        tm_lst_search_per = hdoc.select('//table[@class="search_percent"]//tr//td[@class!="small"]//parent::tr')
        time_lst = []
        for tm_lst_search_per_iter in tm_lst_search_per:
            dict_time = {}
            change = textify(tm_lst_search_per_iter.select('.//td[@class="percent "]/text()'))
            name = textify(tm_lst_search_per_iter.select('.//th//text()'))
            search_percent = textify(tm_lst_search_per_iter.select('.//td[@class="avg "]//text()'))
            dict_time['change'] = change
            dict_time['name'] = name
            dict_time['search_percent'] = search_percent
            time_lst.append(dict_time)
        dict_searp['desc'] = search_percent_description
        dict_searp['time list'] = time_lst
        item.set('Tr_SearchPercent',dict_searp)

        #where visitors go
        dict_wvg = {}
        where_visitors_go = hdoc.select('//div[@id="where-visitors-go"]//div[contains(@class,"tr1")]//p//parent::div')
        subdomain_lst = []
        for where_visitors_go_iter in where_visitors_go:
            dict_subdomain = {}
            site_traffic_percent = textify(where_visitors_go_iter.select('.//p[2]//text()'))
#            site_traffic_percent = textify(site_traffic_percent)
            sub_domain = textify(where_visitors_go_iter.select('.//p[1]//text()'))
            dict_subdomain['site_traffic_percent'] = site_traffic_percent
            dict_subdomain['subdomain'] = sub_domain
            subdomain_lst.append(dict_subdomain)
        dict_wvg['subdomain list'] = subdomain_lst
        item.set('Tr_WherevisitorsGo',dict_wvg)

        #Search Analytics
        #search traffic
        dict_st = {}
        search_traffic_description = textify(hdoc.select('//div[@id="search-traffic"]//p[1]//text()'))
        pl_search_traffic = hdoc.select('//div[@id="search-traffic"]//table[2]//tr')
        period_lst = []
        for pl_search_traffic_iter in pl_search_traffic:
            dict_period = {}
            name = textify(pl_search_traffic_iter.select('.//td[1]//text()'))
            percent_of_search_traffic = textify(pl_search_traffic_iter.select('.//td[2]//text()'))
            dict_period['name'] = name
            dict_period['percent_of_search_traffic'] = percent_of_search_traffic
            period_lst.append(dict_period)
        dict_st['period list'] = period_lst
        dict_st['desc'] = search_traffic_description
        item.set('SA_SearchTraffic',dict_st)

        #top queries from search traffic
        dict_topq = {}
        top_queries_description = textify(hdoc.select('//div[@id="top-keywords-from-search"]/p/text()'))
        query_list = hdoc.select('//div[@id="top-keywords-from-search"]//table[2]//tr')
        query_lst = []
        for query in query_list:
            dict_query = {}
            percent_search_traffic = textify(query.select('.//td[3]//text()'))
            name = textify(query.select('.//td[2]//text()'))
            number = textify(query.select('.//td[1]//text()'))
            dict_query['percent_search_traffic'] = percent_search_traffic
            dict_query['name'] = name
            dict_query['number'] = number
            query_lst.append(dict_query)
        dict_topq['desc'] = top_queries_description
        dict_topq['query list'] = query_lst
        item.set('SA_TopQueries',dict_topq)
        #Search Traffic on the Rise and Decline
        container = hdoc.select('//div/h2[contains(text(),"Search Traffic on the Rise and Decline")]//parent::div')
        search_traffic_rd_description = textify(container.select('.//p/text()'))
        dict_trise = {}
        dict_tdecl = {}
        query_lst = []
        search_query_lst_rise = container.select('//table[@class="dataTable"][2]//tr')
        for search_query in search_query_lst_rise:
            dict_query = {}
            percent_of_search_traffic_rise = textify(search_query.select('.//td[3]'))
            name_rise = textify(search_query.select('.//td[2]'))
            number_rise = textify(search_query.select('.//td[1]'))
            dict_query['percent_of_search_traffic_rise'] = percent_of_search_traffic_rise
            dict_query['name_rise'] = name_rise
            dict_query['number_rise'] = number_rise
            query_lst.append(dict_query)
        dict_trise['desc'] = search_traffic_rd_description
        dict_trise['search query'] = query_lst
        item.set('SA_Trafficrise',dict_trise)

        query_lst = []
        search_query_lst_decl = container.select('//table[@class="dataTable"][4]//tr')
        for search_query in search_query_lst_decl:
            dict_query = {}
            percent_of_search_traffic_decl = textify(search_query.select('.//td[3]'))
            name_decl = textify(search_query.select('.//td[2]'))
            number_decl = textify(search_query.select('.//td[1]'))
            dict_query['percent_of_search_traffic_decl'] = percent_of_search_traffic_decl
            dict_query['name_decl'] = name_decl
            dict_query['number_decl'] = number_decl
            query_lst.append(dict_query)
        dict_tdecl['desc'] = search_traffic_rd_description
        dict_tdecl['search query'] = query_lst
        item.set('SA_Trafficdecl',dict_tdecl)

        #High Impact Search Queries
        dict_highimpsq = {}
        high_impact_description = textify(hdoc.select('//table[@id="kw_general"]//p//text()'))
        hi_container = hdoc.select('//table[@id="kw_general"]')

        lst_query = []
        query_lst = hi_container.select('.//tr//td[3]//parent::tr')
        for query in query_lst:
            dict_query = {}
            name = textify(query.select('.//td[1]//text()'))
            impact_factor = textify(query.select('.//td[2]//text()'))
            query_popularity = textify(query.select('.//td[3]//text()'))
            query_qci = textify(query.select('.//td[4]//text()'))
            dict_query['name'] = name
            dict_query['impact_factor'] = impact_factor
            dict_query['query_popularity'] = query_popularity
            dict_query['query_qci'] = query_qci
            lst_query.append(dict_query)
        dict_highimpsq['desc'] = high_impact_description
        dict_highimpsq['query list'] = lst_query
        item.set('SA_HighImpactSearchQueries',dict_highimpsq)

        #Contact_Info
        name = textify(hdoc.select('//div[@id="contactinfo_div"]/div[1]//strong/text()'))
        contact_det = hdoc.select('//div[@id="contactinfo_div"]/div[1]//text()')
        contact_detail = " ".join(textify(contact_det))
        detail = name + contact_detail

        directory = hdoc.select('//div[@id="contactinfo_div"]//div[2]/@id')

        #company info
        dict_cinfo = {}
        company_info = "".join(textify(hdoc.select('//div[@id="contactinfo_div"]//div[2]//table//text()')))
        contacts_by_dept = "".join(textify(hdoc.select('//div[@id="contactinfo_div"]//div[2]//div[@class="column span-3"][2]//text()')))
        contacts_by_level = "".join(textify(hdoc.select('//div[@id="contactinfo_div"]//div[2]//div[@class="column span-3"][3]//text()')))

        dict_cinfo['detail'] = detail
        dict_cinfo['company info'] = company_info
        dict_cinfo['contacts_by_dept'] = contacts_by_dept
        dict_cinfo['contacts_by_level'] = contacts_by_level

        item.set('Contact Info',dict_cinfo)

        yield item.process()
