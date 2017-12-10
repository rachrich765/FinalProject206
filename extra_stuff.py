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
