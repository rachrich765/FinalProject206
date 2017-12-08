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

zomato_city_id_list = []
#for x in restaurant_name_list:
zomato_city_id = str(city_info['location_suggestions'][0]['id'])
zomato_city_id_list.append(zomato_city_id)
uprint('zomato city_id:', zomato_city_id)
uprint(zomato_city_id_list)

#
CACHE_FNAME2 = "zomato_collections_cache.json"
# either gets new data or caches data, depending upon what the input
#		to search for is.
try:
    # Try to read the data from the file
    cache_file2 = open(CACHE_FNAME2, 'r')
    # If it's there, get it into a string
    cache_contents2 = cache_file2.read()
    # load data into a dictionary
    CACHE_DICTION2 = json.loads(cache_contents2)
    cache_file2.close()
except:
    CACHE_DICTION2 = {}

# #get collection of restaurants per city, total = 100 Restaurants
def get_zomato_collections_in_city(city_id2):
    if city_id2 in CACHE_DICTION2:
        city_collection_results = CACHE_DICTION2[city_id2]
    else:
        base_url7 = 'https://developers.zomato.com/api/v2.1/collections?city_id='
        url7 = base_url7 + city_id2 + '&count=100'
        header7 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response7 = requests.get(url=url7, headers=header7)
        data7 = response7.json()
        city_collection_results = data7
        CACHE_DICTION2[city_id2] = city_collection_results
        fw = open(CACHE_FNAME2,"w")
        fw.write(json.dumps(CACHE_DICTION2))
        fw.close()
    return city_collection_results

for ac in zomato_city_id_list:
    city_collections = get_zomato_collections_in_city(ac)

collection_id_list = []
collection_title_list = []
for ad in city_collections['collections']:
    collection_id = ad['collection']['collection_id']
    collection_id_list.append(collection_id)
    collection_title = ad['collection']['title']
    collection_title_list.append(collection_title)
collection_id_and_title_zip = zip(collection_title_list, collection_id_list)
dict_collection_id_and_title = dict(collection_id_and_title_zip )
print(dict_collection_id_and_title)

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
#
# #get info on restaurants that are in each collection
def get_zomato_restaurants_in_collection(collection):
    if collection in CACHE_DICTION3:
        collection_results = CACHE_DICTION3[collection]
    else:
        base_url8 = 'https://developers.zomato.com/api/v2.1/search?entity_id='
        url8 = base_url8 + zomato_city_id +'&entity_type=city&count=100&collection_id=' + str(collection) +'&sort=rating&order=asc'
        header8 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response8 = requests.get(url=url8, headers=header8)
        data8 = response8.json()
        collection_results = data8
        CACHE_DICTION2[collection] = collection_results
        fw = open(CACHE_FNAME3,"w")
        fw.write(json.dumps(CACHE_DICTION3))
        fw.close()
    return collection_results
#
zomato_restaurant_id_list = []
zomato_restaurant_name_list = []
for x in dict_collection_id_and_title:
    restaurants_in_collection_in_city = get_zomato_restaurants_in_collection(x)
    for y in restaurants_in_collection_in_city['restaurants']:
        #print(x)
        #uprint(y['restaurant'])
        #print('\n')
        zomato_restaurant_id = y['restaurant']['R']['res_id']
        zomato_restaurant_id_list.append(zomato_restaurant_id)
        zomato_restaurant_name = y['restaurant']['name']
        zomato_restaurant_name_list.append(zomato_restaurant_name)
        restaurant_address = y['restaurant']['location']['address']
        restaurant_city = y['restaurant']['location']['city']
        restaurant_locality = y['restaurant']['location']['locality_verbose']
        restaurant_lat = y['restaurant']['location']['latitude']
        restaurant_long = y['restaurant']['location']['longitude']
        restaurant_cuisines = y['restaurant']['cuisines']
        #avg_cost_2 = y['restaurant']['average_cost_for_two']
        zomato_price_range = y['restaurant']['price_range']
        zomato_rating = y['restaurant']['user_rating']['aggregate_rating']
        zomato_rating_text =  y['restaurant']['user_rating']['rating_text']
        zomato_rating_votes = y['restaurant']['user_rating']['votes']
        # uprint('restaurant zomato id:', zomato_restaurant_id)
        # uprint('address:', restaurant_address)
        # uprint('longitude:', restaurant_lat)
        # uprint('lattitude:', restaurant_long)
        # #uprint('average cost for two: $', avg_cost_2)
        # uprint('zomato price range:', zomato_price_range )
        # uprint('zomato_rating:', zomato_rating)
        # uprint('zomato_rating_text:',zomato_rating_text)
        # uprint('zomato_rating_votes:', zomato_rating_votes)


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

# #get restaurant reviews from zomato API
def get_zomato_restaurant_reviews(restaurant_id1):
    if restaurant_id1 in CACHE_DICTION4:
        review_results = CACHE_DICTION4[restaurant_id1]
    else:
        base_url9 = 'https://developers.zomato.com/api/v2.1/reviews?res_id='
        url9 = base_url9 + str(restaurant_id1)
        header9 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response9 = requests.get(url=url9, headers=header9)
        data9 = response9.json()
        review_results = data9
        CACHE_DICTION2[restaurant_id1] = review_results
        fw = open(CACHE_FNAME4,"w")
        fw.write(json.dumps(CACHE_DICTION4))
        fw.close()
    return review_results
#
for y in zomato_restaurant_id_list:
    restaurant_reviews = get_zomato_restaurant_reviews(y)
    uprint(restaurant_reviews)
    for x in restaurant_reviews['user_reviews']:
        zomato_review_text = x['review']['review_text']
        zomato_review_time_posted = x['review']['timestamp']
        #z_reviewer_name = x['review']['user']['name']
        z_reviewer_f_level = x['review']['user']['foodie_level']
        z_reviewer_f_level_num = x['review']['user']['foodie_level_num']
        # uprint('zomato review text:', zomato_review_text)
        # uprint('zomato review posted:', zomato_review_time_posted)
        # uprint('zomato reviewer name:', z_reviewer_f_level)
        # uprint('zomato foodie level:', z_reviewer_f_level)
        # uprint('zomato foodie level number:', z_reviewer_f_level_num)

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
        base_url2 =  'https://api.foursquare.com/v2/venues/'
        url2 = base_url2 + foursquare_restaurant
        params2 = dict(client_id= Keys_and_Secrets.my_id_foursquare, client_secret= Keys_and_Secrets.my_secret_foursquare,
        v='20170801', limit = 1)
        foursquare_restaurant_info = requests.get(url=url2, params=params2)
        foursqaure_restaurant_results = foursquare_restaurant_info
        CACHE_DICTION5[foursquare_restaurant] = foursqaure_restaurant_results
        fw = open(CACHE_FNAME5,"w")
        fw.write(json.dumps(CACHE_DICTION5))
        fw.close()
    return foursqaure_restaurant_results
#
# #get info on restaurant from foursquare API
for restaurant in zomato_restaurant_name_list:
    restaurant_info_foursquare = get_foursquare_restaurant_info(restaurant)

agree_count_list = []
text_of_tips_list = []
tip_text_time_posted_and_agree_counts = {}
foursquare_tip_time_created_list = []
tipper_id_list = []
tipper_first_name_list = []

#get additional info on reviews of restaurant through foursquare
for ae in restaurant_info_foursquare['response']['venue']:
    foursquare_rating = ae['response']['venue']['rating']
    #uprint(foursquare_rating)

for x in restaurant_info_foursquare['response']['venue']['tips']['groups'][0]['items']:
    foursquare_text_tips = x['text']
    text_of_tips_list.append(foursquare_text_tips)
    agreen_count_foursquare_tip = x['agreeCount']
    agree_count_list.append(agreen_count_foursquare_tip)
    time_created_at_foursquare_tip = x['createdAt']
    foursquare_tip_time_created_list.append(time_created_at_foursquare_tip)
    foursquare_tipper_id = x['user']['id']
    tipper_id_list.append(foursquare_tipper_id)
    foursquare_tipper_name = x['user']['firstName']
    tipper_first_name_list.append(foursquare_tipper_name)

#get time during day, day of week, and date of tip (review) posted on foursquare
day = ''
for a in foursquare_tip_time_created_list:
    a1 = time.gmtime(a)
    if a1[6] == 6:
        day = 'Sunday'
    if a1[6] == 5:
        day = 'Saturday'
    if a1[6] == 4:
        day = 'Friday'
    if a1[6] == 3:
        day = 'Thursday'
    if a1[6] == 2:
        day = 'Wednesday'
    if a1[6] == 1:
        day = 'Tuesday'
    if a1[6] == 0:
        day = 'Monday'
    hour_posted = str(a1[3])
    min_posted = str(a1[4])
    hour_and_min_1 = hour_posted + ':' + min_posted
    hour_and_min = datetime.datetime.strptime(hour_and_min_1,'%H:%M').strftime('%I:%M %p')
    if a1[1] == 1:
        print("foursquare review created at:", hour_and_min, day,'January', a1[2], a1[0])
    if a1[1] == 2:
        print("foursquare review created at:", hour_and_min, day, 'February', a1[2], a1[0])
    if a1[1] == 3:
        print("foursquare review created at:", hour_and_min, 'March', a1[2], a1[0])
    if a1[1] == 4:
        print("foursquare review created at:", hour_and_min,day, 'April', a1[2], a1[0])
    if a1[1] == 5:
        print("foursquare review created at:", hour_and_min,day,'May', a1[2], a1[0])
    if a1[1] == 6:
        print("foursquare review created at:", hour_and_min,day, 'June', a1[2], a1[0])
    if a1[1] == 7:
        print("foursquare review created at:", hour_and_min,day, 'July', a1[2], a1[0])
    if a1[1] == 8:
        print("foursquare review created at:", hour_and_min,day, 'August', a1[2], a1[0])
    if a1[1] == 9:
        print("foursquare review created at:", hour_and_min,day, 'September', a1[2], a1[0])
    if a1[1] == 10:
        print("foursquare review created at:", hour_and_min,day, 'October', a1[2], a1[0])
    if a1[1] == 11:
        print("foursquare review created at:", hour_and_min,day, 'November', a1[2], a1[0])
    if a1[1] == 12:
        print("foursquare review created at:", hour_and_min,day, 'December', a1[2], a1[0])

CACHE_FNAME6 = "zomato_restaurants_cache.json"
# # either gets new data or caches data, depending upon what the input
# #		to search for is.
try:
    # Try to read the data from the file
    cache_file6 = open(CACHE_FNAME6, 'r')
    # If it's there, get it into a string
    cache_contents6 = cache_file6.read()
    # load data into a dictionary
    CACHE_DICTION6 = json.loads(cache_contents6)
    cache_file6.close()
except:
    CACHE_DICTION6 = {}
#
def get_google_restaurant_info(google_restaurant):
    if google_restaurant in CACHE_DICTION6:
        google_restaurant_results = CACHE_DICTION6[google_restaurant]
    else:
        lat_long_for_google = str(restaurant_lat) + ' ' + str(restaurant_long)
        base_url3 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        url3 = base_url3 + 'location=' + lat_long_for_google + '&rankby=distance' + '&type=restaurant' + '&keyword=' + ab + '&key=' + Keys_and_Secrets.google_places_key
        resp3 = requests.get(url=url3)
        google_restaurant_info = requests.get(url=url3, params=params3)
        google_restaurant_results = google_restaurant_info
        CACHE_DICTION6[google_restaurant] = google_restaurant_results
        fw = open(CACHE_FNAME6,"w")
        fw.write(json.dumps(CACHE_DICTION6))
        fw.close()
    return google_restaurant_results
#
# #get google info on price level and rating
for ab in zomato_restaurant_name_list:
    google_restaurant_info = get_google_restaurant_info(ab)

if "price_level" in google_restaurant_info['results'][0]:
    google_price_level = google_restaurant_info['results'][0]['price_level']
    uprint('google_price_level:', google_price_level)
    if "rating" in data3['results'][0]:
        google_places_rating = google_restaurant_info['results'][0]['rating']
        uprint('google_places_rating:', google_places_rating)

#
#normalize scores from each API to make it a better comparison
normalized_foursquare_rating = foursquare_rating / 10
normalized_google_place_rating = google_places_rating / 5
normalized_zomato_rating = float(zomato_rating) / 5
uprint('normalized foursquare rating:' , normalized_foursquare_rating)
uprint('normalized google places rating:', normalized_google_place_rating)
uprint('normalized zomato rating', normalized_zomato_rating)
#
# # # #creating database
# # conn = sqlite3.connect('FinalProject.sqlite')
# # cur = conn.cursor()
# # cur.execute("DROP TABLE IF EXISTS Venues")
# # cur.execute("CREATE TABLE Venues (venue_id TEXT, venu_name TEXT)")
# # # #TEXT, venue_name
# # #TEXT, venue_description TEXT, venue_full_address)")
# # tw['response']['vene']['id'],tw['response']['venue']['name']
# #for tw in venue_info:
# #     #tw['response']['venue']['description'], tw['response']['venue']['location']['address']
# #     #venue_description, venue_full_address)
# #     #cur.execute("INSERT INTO Users (venue_id, venue_name, VALUES (?, ?)", tup)
# # conn.commit()
#
# # conn = sqlite3.connect('206_APIsAndDBs.sqlite')
# # cur = conn.cursor()
# # cur.execute('DROP TABLE IF EXISTS Reviews')
# # cur.execute("CREATE TABLE Foursquare Tips (name TEXT, rating NUMBER, review TEXT, agreements NUMBER)")
# for tw in venue_info:
#     tup = tw['response']['venue']['name'], tw['response']['venue']['rating'],
# cur.execute("INSERT INTO Tweets (name, review, user_posted, agreements) VALUES (?, ?, ?, ?)", tup)
# conn.commit()

# cur.execute('DROP TABLE IF EXISTS Popular Hours')
# cur.execute("CREATE TABLE Popular Hours (name TEXT, popular_hours NUMBER)")
# for tw in venue_info:
#     tup = tw['response']['venue']['name'], tw['response']['venue']['popular']
# cur.execute("INSERT INTO Popular Hours (name, here_now, popular_hours) VALUES (?, ?, ?)", tup)
