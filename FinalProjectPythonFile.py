## SI 206 2017
## Project 4
import operator
import unittest
import itertools
import collections
import json
import sqlite3
import sys
import requests
from pprint import pprint
import Keys_and_Secrets
import time
import datetime


# Your name:Rachel Richardson

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

city = input('enter city: ')

CACHE_FNAME1 = "zomato_city_cache.json"
# either gets new data or caches data, depending upon what the input
#		to search for is.
try:
    # Try to read the data from the file
    cache_file1 = open(CACHE_FNAME1, 'r')
    # If it's there, get it into a string
    cache_contents1 = cache_file1.read()
    # load data into a dictionary
    CACHE_DICTION1 = json.loads(cache_contents1)
    cache_file1.close()
except:
    CACHE_DICTION1 = {}

# Define your function get_user_tweets here:
def get_zomato_city(city):
    if city in CACHE_DICTION1:
        city_results = CACHE_DICTION1[city]
    else:
        base_url6 = 'https://developers.zomato.com/api/v2.1/cities?q='
        url6 = base_url6 + city
        header6 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response6 = requests.get(url=url6, headers=header6)
        data6 = response6.json()
        #uprint(data6)
        city_results = data6
        CACHE_DICTION1[city] = city_results
        fw = open(CACHE_FNAME1,"w")
        fw.write(json.dumps(CACHE_DICTION1))
        fw.close()
    return city_results
#get city id for city
city_info = get_zomato_city(city)

zomato_city_id = str(city_info['location_suggestions'][0]['id'])

#uprint('zomato city_id:', zomato_city_id)
# #

CACHE_FNAME3 = "zomato_restaurants_cache.json"
# # either gets new data or caches data, depending upon what the input
# #		to search for is.
try:
#     # Try to read the data from the file
    cache_file3 = open(CACHE_FNAME3, 'r')
#If it's there, get it into a string
    cache_contents3 = cache_file3.read()
#     # load data into a dictionary
    CACHE_DICTION3 = json.loads(cache_contents3)
    cache_file3.close()
except:
    CACHE_DICTION3 = {}

#get info on restaurants that are in each collection
def get_zomato_restaurants_in_collection(collection):
    if collection in CACHE_DICTION3:
        collection_results = CACHE_DICTION3[collection]
    else:
        base_url8 = 'https://developers.zomato.com/api/v2.1/search?entity_id='
        url8 = base_url8 + zomato_city_id +'&entity_type=city&count=25&collection_id=1&radius=0&sort=rating&order=asc'
        header8 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response8 = requests.get(url=url8, headers=header8)
        data8 = response8.json()
        collection_results = data8
        CACHE_DICTION3[collection] = collection_results
        fw = open(CACHE_FNAME3,"w")
        fw.write(json.dumps(CACHE_DICTION3))
        fw.close()
    return collection_results
collection = str(1)
restaurants_info = get_zomato_restaurants_in_collection(collection)
zomato_restaurant_id_list = []
zomato_restaurant_name_list = []
restaurant_address_list = []
restaurant_locality_list = []
restaurant_cuisine_list = []
zomato_review_text_list = []
zomato_rating_text_list = []
zomato_rating_list = []
zomato_rating_votes_list = []
zomato_price_range_list = []
avg_cost_2_list = []
for y in restaurants_info['restaurants']:
    #uprint(y['restaurant'])
    zomato_restaurant_id = str(y['restaurant']['R']['res_id'])
    zomato_restaurant_id_list.append(zomato_restaurant_id)
    zomato_restaurant_name = y['restaurant']['name']
    zomato_restaurant_name_list.append(zomato_restaurant_name)
    restaurant_address = y['restaurant']['location']['address']
    restaurant_address_list.append(restaurant_address)
    restaurant_locality = y['restaurant']['location']['locality_verbose']
    restaurant_locality_list.append(restaurant_locality)
    restaurant_lat = y['restaurant']['location']['latitude']
    restaurant_long = y['restaurant']['location']['longitude']
    restaurant_cuisines = y['restaurant']['cuisines']
    restaurant_cuisine_list.append(restaurant_cuisines)
    zomato_price_range = y['restaurant']['price_range']
    zomato_price_range_list.append(zomato_price_range)
    zomato_rating = y['restaurant']['user_rating']['aggregate_rating']
    zomato_rating_list.append(zomato_rating)
    zomato_rating_text =  y['restaurant']['user_rating']['rating_text']
    zomato_rating_text_list.append(zomato_rating_text)
    zomato_rating_votes = y['restaurant']['user_rating']['votes']
    zomato_rating_votes_list.append(zomato_rating_votes)
    avg_cost_2 = y['restaurant']['average_cost_for_two']
    avg_cost_2_list.append(avg_cost_2)
# #         # uprint('restaurant zomato id:', zomato_restaurant_id)
#         # uprint('address:', restaurant_address)
#         # uprint('longitude:', restaurant_lat)
#         # uprint('lattitude:', restaurant_long)
#         # #uprint('average cost for two: $', avg_cost_2)
#         # uprint('zomato price range:', zomato_price_range )
#         # uprint('zomato_rating:', zomato_rating)
#         # uprint('zomato_rating_text:',zomato_rating_text)
#         # uprint('zomato_rating_votes:', zomato_rating_votes)

#
CACHE_FNAME4 = "zomato_reviews_cache.json"
# # either gets new data or caches data, depending upon what the input
# #		to search for is.
try:
#     # Try to read the data from the file
    cache_file4 = open(CACHE_FNAME4, 'r')
#     # If it's there, get it into a string
    cache_contents4 = cache_file4.read()
#     # load data into a dictionary
    CACHE_DICTION4 = json.loads(cache_contents4)
    cache_file4.close()
except:
    CACHE_DICTION4 = {}
#
# # # #get restaurant reviews from zomato API
def get_zomato_restaurant_reviews(restaurant_id1):
    if restaurant_id1 in CACHE_DICTION4:
        review_results = CACHE_DICTION4[restaurant_id1]
    # else:
    #     base_url9 = 'https://developers.zomato.com/api/v2.1/reviews?res_id='
    #     url9 = base_url9 + restaurant_id1 + '&count=1'
    #     header9 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
    #     response9 = requests.get(url=url9, headers=header9)
    #     data9 = response9.json()
    #     review_results = data9
    #     CACHE_DICTION4[restaurant_id1] = review_results
    #     fw = open(CACHE_FNAME4,"w")
    #     fw.write(json.dumps(CACHE_DICTION4))
    #     fw.close()
    return review_results

zomato_reviewer_name_list = []
zomato_review_text_list = []
zomato_reviewer_foodie_level_word_list = []
zomato_reviewer_foodie_level_number_list = []
zomato_time_review_posted_list = []
for y in zomato_restaurant_id_list:
    restaurant_reviews = get_zomato_restaurant_reviews(y)
    for x in restaurant_reviews['user_reviews']:
        #uprint(x['review']['likes'])
        zomato_review_text = x['review']['review_text']
        zomato_review_text_list.append(zomato_review_text)
        zomato_review_time_posted1 = x['review']['timestamp']
        zomato_time_review_posted_list.append(zomato_review_time_posted1)
        z_reviewer_name = x['review']['user']['name']
        zomato_reviewer_name_list.append(z_reviewer_name)
        z_reviewer_f_level = x['review']['user']['foodie_level']
        zomato_reviewer_foodie_level_word_list.append(z_reviewer_f_level)
        z_reviewer_f_level_num = x['review']['user']['foodie_level_num']
        zomato_reviewer_foodie_level_number_list.append(z_reviewer_f_level_num)
#         uprint(y, 'zomato review text:', zomato_review_text)
#         uprint(y, 'zomato review posted:', zomato_review_time_posted)
#         uprint(y, 'zomato reviewer name:', z_reviewer_f_level)
#         uprint(y, 'zomato foodie level:', z_reviewer_f_level)
#         uprint(y, 'zomato foodie level number:', z_reviewer_f_level_num)
zomato_time_review_posted_list2 = []
for f in zomato_time_review_posted_list:
    f1 = time.gmtime(f)
    zomato_review_time_posted2 = time.strftime("%c", f1)
    zomato_time_review_posted_list2.append(zomato_review_time_posted2)
    #print(zomato_review_time_posted2)
        #month_number = g[7:9]
        #print(month_number)
        #hour_posted = str(a1[3])
        #min_posted = str(a1[4])
        #hour_and_min_1 = hour_posted + ':' + min_posted
        #hour_and_min = datetime.datetime.strptime(hour_and_min_1,'%H:%M').strftime('%I:%M %p')
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
        params2 = dict(client_id = Keys_and_Secrets.my_id_foursquare, client_secret = Keys_and_Secrets.my_secret_foursquare, v = '20171009', near = city, query = foursquare_restaurant, category = '4d4b7105d754a06374d81259', limit = 1)
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
#get additional info on reviews of restaurant through foursquare
    for x in foursquare_restaurant_info:
        restaurant_foursquare = x['response']['venues']
        #print(restaurant_foursquare)
        for y in restaurant_foursquare:
            foursquare_id = (y['id'])
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
        params10 = dict(client_id = Keys_and_Secrets.my_id_foursquare, client_secret = Keys_and_Secrets.my_secret_foursquare, v = '20171009', limit = 1)
        response10 = requests.get(url=url10, params=params10)
        data10 = response10.json()
        foursqaure_review_results = data10
        CACHE_DICTION10[foursquare_restaurant_id] = foursqaure_review_results
        fw = open(CACHE_FNAME10,"w")
        fw.write(json.dumps(CACHE_DICTION10))
        fw.close()
    return foursqaure_review_results

foursquare_tip_time_created_list = []
agree_count_list = []
foursquare_tip_text_list = []
foursquare_tipper_id_list = []
tipper_name_list = []
foursquare_rating_list = []
for abc in foursquare_id_list:
    tips_info = get_foursquare_review_info(abc)
    visits_count = tips_info['response']['venue']['stats']['visitsCount']
    visits_count_list.append(visits_count)
    if "rating" in tips_info['response']['venue']:
        foursquare_rating = tips_info['response']['venue']['rating']
        foursquare_rating_list.append(foursquare_rating)
    if len(tips_info['response']['venue']['tips']['groups']) > 0:#[0]['items']) > 0:
        abcde = tips_info['response']['venue']['tips']['groups']
        for x in abcde:
            tips_stuff1 = x['items']
            for z in foursquare_id_list:
                for y in tips_stuff1:
                    foursquare_tip_time_created = y['createdAt']
                    foursquare_tip_time_created_list.append(foursquare_tip_time_created)
                    foursqaure_tip_text = y['text']
                    foursquare_tip_text_list.append(foursqaure_tip_text)
                    agreen_count_foursquare_tip = y['agreeCount']
                    agree_count_list.append(agreen_count_foursquare_tip)
                    if "user" in y:
                        foursquare_tipper_id = y['user']['id']
                        foursquare_tipper_id_list.append(foursquare_tipper_id)
                        foursquare_tipper_first_name = y['user']['firstName']
                        if "lastName" in y['user']:
                            last_name_tipper = y['user']['lastName']
                            tipper_name = foursquare_tipper_first_name + " " + last_name_tipper
                            tipper_name_list.append(tipper_name)
                            tipper_name = foursquare_tipper_first_name
                            tipper_name_list.append(tipper_name)
#uprint(zomato_restaurant_name, foursquare_tip_text_list)

# # #get time during day, day of week, and date of tip (review) posted on foursquare
foursquare_tip_time_created_list2 = []
for a in foursquare_tip_time_created_list:
    a1 = time.gmtime(a)
    foursquare_tip_time_created = time.strftime("%c", a1)
    foursquare_tip_time_created_list2.append(foursquare_tip_time_created)
    #print(foursquare_tip_time_created)
CACHE_FNAME6 = "google_restaurants_cache.json"
# # # either gets new data or caches data, depending upon what the input
# # #		to search for is.
cache_file6 = open(CACHE_FNAME6, 'r')
try:
    cache_contents6 = cache_file6.read()
    CACHE_DICTION6 = json.loads(cache_contents6)
    cache_file6.close()
except:
    CACHE_DICTION6 = {}
# #
def get_google_restaurant_info(google_restaurant):
    if google_restaurant in CACHE_DICTION6:
        google_restaurant_results = CACHE_DICTION6[google_restaurant]
    else:
        lat_long_for_google = str(restaurant_lat) + ' ' + str(restaurant_long)
        base_url3 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        url3 = base_url3 + 'location=' + lat_long_for_google + '&rankby=distance' + '&type=restaurant' + '&keyword=' + ab + '&key=' + Keys_and_Secrets.google_places_key
        resp3 = requests.get(url=url3)
        data3 = resp3.json()
        google_restaurant_results = data3
        CACHE_DICTION6[google_restaurant] = google_restaurant_results
        fw = open(CACHE_FNAME6,"w")
        fw.write(json.dumps(CACHE_DICTION6))
        fw.close()
    return google_restaurant_results

google_places_rating_list = []
google_price_level_list = []
# #get google info on price level and rating
i = 0
while i < 25:
    for ab in zomato_restaurant_name_list:
        google_restaurant_info = get_google_restaurant_info(ab)
        i += 1
        try:
            gotdata = google_restaurant_info['results'][0]
            if "rating" in google_restaurant_info['results'][0]:
                google_places_rating = google_restaurant_info['results'][0]['rating']
                google_places_rating_list.append(google_places_rating)
                normalized_google_place_rating = google_places_rating / 5
            if "price_level" in google_restaurant_info['results'][0]:
                google_price_level = google_restaurant_info['results'][0]['price_level']
                google_price_level_list.append(google_price_level)
        except IndexError:
            gotdata = 'null'

# #normalize scores from each API to make it a better comparison

zip_general_restaurant_info = zip(zomato_restaurant_name_list, restaurant_address_list, restaurant_locality_list, restaurant_cuisine_list)
zip_interactions_zomato_part_1 = zip(zomato_restaurant_name_list, zomato_rating_list, avg_cost_2_list, zomato_price_range_list)
zip_interactions_google = zip(zomato_restaurant_name_list, google_places_rating_list, google_price_level_list)
zip_interactions_zomato_part_2 = zip(zomato_restaurant_name_list, zomato_review_text_list, zomato_time_review_posted_list2, zomato_reviewer_name_list, zomato_reviewer_foodie_level_word_list, zomato_reviewer_foodie_level_number_list)
zip_interactions_foursquare_part1 = zip(zomato_restaurant_name_list, foursquare_rating_list, visits_count_list)
#foursquare_tip_text_list, foursquare_tip_time_created_list2, agree_count_list, foursquare_tipper_id_list ,tipper_name_list
zip_tips_foursquare = zip(zomato_restaurant_name_list, foursquare_tip_text_list, foursquare_tip_time_created_list2, agree_count_list, foursquare_tipper_id_list ,tipper_name_list)
normalized_zomato_rating = float(zomato_rating) / 5
normalized_google_rating = (google_places_rating) / 5
normalized_foursquare_rating = foursquare_rating / 10

# # #creating database
conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS General_Restaurant_Info")
cur.execute("CREATE TABLE General_Restaurant_Info (restaurant_name TEXT, restaurant_address TEXT, restaurant_locality TEXT, restaurant_cuisines TEXT)")
for y in zip_general_restaurant_info:
    tup = y[0], y[1], y[2], y[3]
    cur.execute("INSERT INTO General_Restaurant_Info (restaurant_name, restaurant_address, restaurant_locality, restaurant_cuisines) VALUES (?, ?, ?, ?)", tup)
conn.commit()

conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Zomato_Interactions_Part_1')
cur.execute("CREATE TABLE Zomato_Interactions_Part_1 (restaurant_name TEXT, zomato_rating_out_of_5 NUMBER,average_cost_for_two NUMBER, zomato_price_range_out_of_5 NUMBER)")
for y in zip_interactions_zomato_part_1:
    tup = y[0], y[1], y[2], y[3]
    cur.execute("INSERT INTO Zomato_Interactions_Part_1 (restaurant_name, zomato_rating_out_of_5,average_cost_for_two, zomato_price_range_out_of_5) VALUES (?, ?, ?, ?)", tup)
conn.commit()
#
conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Interactions_Part_2_Zomato_Reviews')
cur.execute("CREATE TABLE Interactions_Part_2_Zomato_Reviews (restaurant_name TEXT, zomato_review_text TEXT, zomato_time_review_posted TEXT, zomato_reviewer_name TEXT, zomato_reviewer_foodie_level_word TEXT,zomato_reviewer_foodie_level_number TEXT)")
for y in zip_interactions_zomato_part_2:
    tup = y[0], y[1], y[2], y[3], y[4], y[5]
    cur.execute("INSERT INTO Interactions_Part_2_Zomato_Reviews (restaurant_name, zomato_review_text, zomato_time_review_posted, zomato_reviewer_name, zomato_reviewer_foodie_level_word,zomato_reviewer_foodie_level_number) VALUES (?, ?, ?, ?, ?, ?)", tup)
conn.commit()

conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Google_Interactions')
cur.execute("CREATE TABLE Google_Interactions (restaurant_name TEXT, google_rating_out_of_5 NUMBER, google_price_range_out_of_5 NUMBER)")
for y in zip_interactions_google:
    tup = y[0], y[1], y[2]
    cur.execute("INSERT INTO Google_Interactions (restaurant_name, google_rating_out_of_5, google_price_range_out_of_5) VALUES (?, ?, ?)", tup)
conn.commit()

conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Foursquare_Interactions_Part1')
cur.execute("CREATE TABLE Foursquare_Interactions_Part1 (restaurant_name TEXT, foursquare_rating NUMBER, visits_count NUMBER)")
for y in zip_interactions_foursquare_part1:
    tup = y[0], y[1], y[2]
    cur.execute("INSERT INTO Foursquare_Interactions_Part1 (restaurant_name, foursquare_rating, visits_count) VALUES (?, ?, ?)", tup)
conn.commit()

conn = sqlite3.connect('FinalProject.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Foursquare_Tips')
cur.execute("CREATE TABLE Foursquare_Tips (restaurant_name TEXT, tip_text TEXT, time_tip_posted TEXT, number_of_likes_on_tip NUMBER, tipper_foursqaure_id NUMBER, name_of_tipper TEXT)")
for x in zomato_restaurant_name_list:
    for y in zip_tips_foursquare:
        tup = y[0], y[1], y[2], y[3], y[4], y[5]
        cur.execute("INSERT INTO Foursquare_Tips (restaurant_name, tip_text, time_tip_posted, number_of_likes_on_tip, tipper_foursqaure_id, name_of_tipper) VALUES (?, ?, ?, ?, ?, ?)", tup)
conn.commit()
#tip_text TEXT, time_tip_posted TEXT, number_of_likes_on_tip NUMBER, tipper_foursqaure_id NUMBER, name_of_tipper TEXT
