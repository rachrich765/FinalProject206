#get info for restaurant on zomato
base_url5 = "https://developers.zomato.com/api/v2.1/search?q="
given_place_len_minius1 = (len(given_place.split()) - 1)
i = 0
given_place_zomato_step1 = ''
while i < (given_place_len_minius1):
    for x in given_place.split():
        i += 1
        given_place_zomato_step1 += (x+'%20')
l = list(given_place_zomato_step1)
del(l[-3:])
given_place_zomato_step2 = "".join(l)  # convert back to string
if 'the%20' in given_place_zomato_step2:
    given_place_zomato_step2 = given_place_zomato_step2.replace('the%20', '')
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
url5 = base_url5 + given_place_zomato_step2 +'&lat=' + str(lat_venue) + '&lon=%20' + str(long_venue) + "&radius=0&sort=real_distance&order=assc"
response5 = requests.get(url=url5, headers=header)
data5 = response5.json()
avg_cost_2 = data5['restaurants'][0]['restaurant']['average_cost_for_two']
uprint('average cost for 2 people:', '$', avg_cost_2)
locality = data5['restaurants'][0]['restaurant']['location']['locality_verbose']
price_range_zomato = data5['restaurants'][0]['restaurant']['price_range']
uprint('price range:', price_range_zomato)
zomato_res_id = (data5['restaurants'][0]['restaurant']['R']['res_id'])
zomato_rating = (data5['restaurants'][0]['restaurant']['user_rating']['aggregate_rating'])
zomato_votes_rating = (data5['restaurants'][0]['restaurant']['user_rating']['votes'])


#get info on city
# venue_info = get_place_info(given_place)
# lat_venue = str(venue_info['response']['venue']['location']['lat'])
# long_venue = str(venue_info['response']['venue']['location']['lng'])
# base_url4 = 'https://developers.zomato.com/api/v2.1/geocode?'
# url4 = base_url4 + 'lat=' + lat_venue + '&lon=' + long_venue
# header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
# response = requests.get(url=url4, headers=header)
# data4 = response.json()
# #uprint(data4)
# location_title = data4['location']['title']
# city_popularity = data4['popularity']['popularity']
# city_nighlife_rating = data4['popularity']['nightlife_index']
# # uprint('city popularity:', city_popularity, '/ 5')
# # uprint('city night life rating:', city_nighlife_rating, '/ 5')
# #city_best_food_types = data4['popularity']['top_cuisines']
# #uprint("city best food types:", city_best_food_types)


#uprint("venue name:", venue_name)
#uprint("venue_full_address:", venue_full_address)
# uprint("foursqure_rating:", foursqure_rating)
# uprint("foursquare visits to restaurant count:", visits_count)
# uprint("foursquare text_of_tips_list:",text_of_tips_list)
# uprint("foursquare agree_count_list:",agree_count_list)
# uprint("foursquare time_created_list:", time_created_list)
# uprint(" foursquare lat_venue,long_venue:", lat_venue,long_venue)
# uprint("foursquare tipper_first_name_list:", tipper_first_name_list)
# uprint("foursquare tipper_id_list:", tipper_id_list)
visits_count = venue_info['response']['venue']['stats']['visitsCount']


        # day_list = []
        # popular_time_list = []
        # days_and_popular_times_dict = {}
        # if 'popular' in foursquare_dict.keys():
        #     for x in venue_info['response']['venue']['popular']['timeframes']:
        #         day_list.append([x][0]['days'])
        #         popular_time_list.append([x][0]['open'][0]['renderedTime'])
        #         days_and_popular_times_zip_dict = zip(day_list, popular_time_list)
        #         days_and_popular_times_dict = dict(days_and_popular_times_zip_dict)
        #         uprint("days and thier popular times from foursquare", days_and_popular_times_dict)
        # uprint('cuisines:', restaurant_cuisines)
                # uprint('locality:', restaurant_locality)
                        # uprint('city:', restaurant_city)
#avg_cost_2 = y['restaurant']['average_cost_for_two']


# CACHE_FNAME2 = "zomato_collections_cache.json"
# # either gets new data or caches data, depending upon what the input
# #		to search for is.
# try:
#     # Try to read the data from the file
#     cache_file2 = open(CACHE_FNAME2, 'r')
#     # If it's there, get it into a string
#     cache_contents2 = cache_file2.read()
#     # load data into a dictionary
#     CACHE_DICTION2 = json.loads(cache_contents2)
#     cache_file2.close()
# except:
#     CACHE_DICTION2 = {}
#
# # # #get collection of restaurants per city, total = 25 Restaurants
# def get_zomato_collections_in_city(city_id2):
#     if city_id2 in CACHE_DICTION2:
#         city_collection_results = CACHE_DICTION2[city_id2]
#     else:
#         base_url7 = 'https://developers.zomato.com/api/v2.1/collections?city_id='
#         url7 = base_url7 + city_id2 + '&count=1'
#         header7 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
#         response7 = requests.get(url=url7, headers=header7)
#         data7 = response7.json()
#         city_collection_results = data7
#         CACHE_DICTION2[city_id2] = city_collection_results
#         fw = open(CACHE_FNAME2,"w")
#         fw.write(json.dumps(CACHE_DICTION2))
#         fw.close()
#     return city_collection_results
# print(zomato_city_id)
#city_collections = get_zomato_collections_in_city(zomato_city_id)
#uprint(city_collections)
# collection_id_list = []
# collection_title_list = []
# for ad in city_collections['collections']:
#     collection_id = ad['collection']['collection_id']
#     collection_id_list.append(collection_id)
#     collection_title = ad['collection']['title']
#     collection_title_list.append(collection_title)
# collection_id_and_title_zip = zip(collection_title_list, collection_id_list)
# dict_collection_id_and_title = dict(collection_id_and_title_zip )
# print(dict_collection_id_and_title)
    # a1 = time.gmtime(a)
    # if a1[6] == 6:
    #     day = 'Sunday'
    # if a1[6] == 5:
    #     day = 'Saturday'
    # if a1[6] == 4:
    #     day = 'Friday'
    # if a1[6] == 3:
    #     day = 'Thursday'
    # if a1[6] == 2:
    #     day = 'Wednesday'
    # if a1[6] == 1:
    #     day = 'Tuesday'
    # if a1[6] == 0:
    #     day = 'Monday'
    # hour_posted = str(a1[3])
    # min_posted = str(a1[4])
    # hour_and_min_1 = hour_posted + ':' + min_posted
    # hour_and_min = datetime.datetime.strptime(hour_and_min_1,'%H:%M').strftime('%I:%M %p')
    # date = day + " " + hour_and_min
    # foursquare_tip_time_created_list2.append(date)
    # if a1[1] == 1:
    #     #print("foursquare review created at:", hour_and_min, day,'January', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'January', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 2:
    #     #print("foursquare review created at:", hour_and_min, day, 'February', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'February', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 3:
    #     #print("foursquare review created at:", hour_and_min, 'March', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'March', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 4:
    #     #print("foursquare review created at:", hour_and_min,day, 'April', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'April', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 5:
    #     #print("foursquare review created at:", hour_and_min,day,'May', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'May', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 6:
    #     #print("foursquare review created at:", hour_and_min,day, 'June', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'June', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 7:
    #     #print("foursquare review created at:", hour_and_min,day, 'July', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'July', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 8:
    #     #print("foursquare review created at:", hour_and_min,day, 'August', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'August', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 9:
    #     #print("foursquare review created at:", hour_and_min,day, 'September', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'September', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 10:
    #     #print("foursquare review created at:", hour_and_min,day, 'October', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'October', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 11:
    #     #print("foursquare review created at:", hour_and_min,day, 'November', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'November', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)
    # if a1[1] == 12:
    #     #print("foursquare review created at:", hour_and_min,day, 'December', a1[2], a1[0])
    #     time_created_format = (hour_and_min, day, 'December', a1[2], a1[0])
    #     #foursquare_tip_time_created_list2.append(time_created_format)
    #     #print(time_created_format)

    CACHE_FNAME5 = "foursquare_restaurants_cache.json"
    # # either gets new data or caches data, depending upon what the input
    # #		to search for is.
    try:
    #     # Try to read the data from the file
        cache_file5 = open(CACHE_FNAME5, 'r')
    #     # If it's there, get it into a string
        cache_contents5 = cache_file5.read()
    #     # load data into a dictionary
        CACHE_DICTION5 = json.loads(cache_contents5)
        cache_file5.close()
    except:
        CACHE_DICTION5 = {}

    def get_foursquare_restaurant_info(foursquare_restaurant):
        if foursquare_restaurant in CACHE_DICTION5:
            foursqaure_restaurant_results = CACHE_DICTION5[foursquare_restaurant]
        else:
            url2 = 'https://api.foursquare.com/v2/venues/search'
            params2 = dict(client_id = Keys_and_Secrets.my_id_foursquare, client_secret = Keys_and_Secrets.my_secret_foursquare, v = '20171009', near = city, query = foursquare_restaurant, category = '4d4b7105d754a06374d81259')
            response2 = requests.get(url=url2, params=params2)
            data2 = response2.json()
            foursqaure_restaurant_results = data2
            CACHE_DICTION5[foursquare_restaurant] = foursqaure_restaurant_results
            fw = open(CACHE_FNAME5,"w")
            fw.write(json.dumps(CACHE_DICTION5))
            fw.close()
        return foursqaure_restaurant_results

    agree_count_list = []
    text_of_tips_list = []
    tip_text_time_posted_and_agree_counts = {}
    foursquare_tip_time_created_list = []
    tipper_id_list = []
    tipper_first_name_list = []
    visits_count_list = []
    foursquare_id_list = []

for ab in zomato_restaurant_name_list:
    foursquare_restaurant_info = get_foursquare_restaurant_info(ab)
    restaurant_foursquare = foursquare_restaurant_info['response']['venues'][0]
            #print(restaurant_foursquare)
    foursquare_id = (restaurant_foursquare['id'])
    foursquare_id_list.append(foursquare_id)
                #foursquare_rating =

    CACHE_FNAME10 = "foursquare_reviews_cache.json"
    try:
    #     # Try to read the data from the file
        cache_file10 = open(CACHE_FNAME10, 'r')
    #     # If it's there, get it into a string
        cache_contents10 = cache_file10.read()
    #     # load data into a dictionary
        CACHE_DICTION10 = json.loads(cache_contents10)
        cache_file10.close()
    except:
        CACHE_DICTION10 = {}
    def get_foursquare_review_info(foursquare_restaurant_id):
        if foursquare_restaurant_id in CACHE_DICTION10:
            foursqaure_review_results = CACHE_DICTION10[foursquare_restaurant_id]
        else:
            base_url10 = 'https://api.foursquare.com/v2/venues/'
            url10 = base_url10 + str(foursquare_restaurant_id)
            params10 = dict(client_id = Keys_and_Secrets.my_id_foursquare, client_secret = Keys_and_Secrets.my_secret_foursquare, v = '20171009', limit = 1, sort = 'popuplar')
            response10 = requests.get(url=url10, params=params10)
            data10 = response10.json()
            foursqaure_review_results = data10
            CACHE_DICTION10[foursquare_restaurant_id] = foursqaure_review_results
            fw = open(CACHE_FNAME10,"w")
            fw.write(json.dumps(CACHE_DICTION10))
            fw.close()
        return foursqaure_review_results

    foursquare_tip_time_created_list = []
    likes_count_foursquare_tip_list = []
    foursquare_tip_text_list = []
    foursquare_tipper_id_list = []
    tipper_name_list = []
    foursquare_rating_list = []
    foursquare_price_tier_list = []
    foursquare_price_tier_translation_list = []

    for abc in foursquare_id_list:
        print(abc)
        tips_info = get_foursquare_review_info(abc)
        visits_count = tips_info['response']['venue']['stats']['visitsCount']
        visits_count_list.append(visits_count)
        if "price" in tips_info['response']['venue']:
            foursquare_price_tier = (tips_info['response']['venue']['price']['tier'])
            foursquare_price_tier_list.append(foursquare_price_tier)
            foursquare_price_tier_translation = tips_info['response']['venue']['price']['message']
            foursquare_price_tier_translation_list.append(foursquare_price_tier_translation)
            #uprint(abc, foursquare_price_tier, foursquare_price_tier_translation)
        if "rating" in tips_info['response']['venue']:
            foursquare_rating = tips_info['response']['venue']['rating']
            foursquare_rating_list.append(foursquare_rating)
        if len(tips_info['response']['venue']['tips']['groups']) > 0:
            abcde = tips_info['response']['venue']['tips']['groups']
            for x in abcde:
                tips_stuff1 = x['items']
                for y in tips_stuff1:
                    foursquare_tip_time_created = y['createdAt']
                    if foursquare_tip_time_created not in foursquare_tip_time_created_list:
                        foursquare_tip_time_created_list.append(foursquare_tip_time_created)
                    foursquare_tip_text = y['text']
                    if foursquare_tip_text not in foursquare_tip_text_list:
                        foursquare_tip_text_list.append(foursquare_tip_text)
                    likes_count_foursquare_tip = y['likes']['count']
                    #uprint(likes_count_foursquare_tip)
                    if likes_count_foursquare_tip not in likes_count_foursquare_tip_list:
                        likes_count_foursquare_tip_list.append(likes_count_foursquare_tip)
                        #uprint(likes_count_foursquare_tip_list)
                    if "user" in y:
                        foursquare_tipper_id = y['user']['id']
                    if foursquare_tipper_id not in foursquare_tipper_id_list:
                        foursquare_tipper_id_list.append(foursquare_tipper_id)
                        foursquare_tipper_first_name = y['user']['firstName']
                        if "lastName" in y['user']:
                            last_name_tipper = y['user']['lastName']
                            tipper_name = foursquare_tipper_first_name + " " + last_name_tipper
                            if tipper_name not in tipper_name_list:
                                tipper_name_list.append(tipper_name)
                        else:
                            tipper_name = foursquare_tipper_first_name
                            if tipper_name not in tipper_name_list:
                                tipper_name_list.append(tipper_name)
                                #uprint(tipper_name_list)
    # uprint(len(foursquare_tip_text))
    # uprint(len(foursquare_tip_time_created_list))
    # uprint(len(foursquare_tipper_id_list))
    # uprint(len(tipper_name_list))
    # # # #get time during day, day of week, and date of tip (review) posted on foursquare
    foursquare_tip_time_created_list2 = []
    for a in foursquare_tip_time_created_list:
        a1 = time.gmtime(a)
        foursquare_tip_time_created = time.strftime("%c", a1)
        foursquare_tip_time_created_list2.append(foursquare_tip_time_created)
