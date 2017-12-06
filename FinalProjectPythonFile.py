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

#get places rating from FourSquare
base_url1 = "https://api.foursquare.com/v2/venues/search?query="
given_place = input('enter place: ')
near_city = input('enter city: ')
params1 = dict( v='20170801', near = near_city, limit=1)
url1 = base_url1 + given_place + "&client_id=" + Keys_and_Secrets.my_id_foursquare + "&client_secret=" + Keys_and_Secrets.my_secret_foursquare + "&intent=browse"
resp1 = requests.get(url=url1, params=params1)
data1 = json.loads(resp1.text)
id_place = data1['response']['venues'][0]['id']

CACHE_FNAME = "206_FinalProject_cache.json"
# either gets new data or caches data, depending upon what the input
#		to search for is.
try:
    # Try to read the data from the file
    cache_file = open(CACHE_FNAME, 'r')
    # If it's there, get it into a string
    cache_contents = cache_file.read()
    # load data into a dictionary
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# Define your function get_user_tweets here:
def get_place_info(place):
    if place in CACHE_DICTION:
        place_results = CACHE_DICTION[place]
    else:
        base_url2 =  'https://api.foursquare.com/v2/venues/'
        url2 = base_url2 + id_place
        params2 = dict(client_id= Keys_and_Secrets.my_id_foursquare, client_secret= Keys_and_Secrets.my_secret_foursquare,
         v='20170801', limit = 1)
        data_places = requests.get(url=url2, params=params2)
        place_results = json.loads(data_places.text)
        CACHE_DICTION[place] = place_results
        fw = open(CACHE_FNAME,"w")
        fw.write(json.dumps(CACHE_DICTION))
        fw.close()
    return place_results

#get info on city
venue_info = get_place_info(given_place)
lat_venue = str(venue_info['response']['venue']['location']['lat'])
long_venue = str(venue_info['response']['venue']['location']['lng'])
base_url4 = 'https://developers.zomato.com/api/v2.1/geocode?'
url4 = base_url4 + 'lat=' + lat_venue + '&lon=' + long_venue
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
response = requests.get(url=url4, headers=header)
data4 = response.json()
#uprint(data4)
location_title = data4['location']['title']
city_popularity = data4['popularity']['popularity']
city_nighlife_rating = data4['popularity']['nightlife_index']
# uprint('city popularity:', city_popularity, '/ 5')
# uprint('city night life rating:', city_nighlife_rating, '/ 5')
# uprint(city_best_food_types)
city_best_food_types = data4['popularity']['top_cuisines']

#get city id for city
base_url6 = 'https://developers.zomato.com/api/v2.1/cities?q='
url6 = base_url6 + near_city
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
response6 = requests.get(url=url6, headers=header)
data6 = response6.json()
city_id = str(data6['location_suggestions'][0]['id'])
#uprint('city_id:', city_id)

# #get collections per city, total = 100 Restaurants
base_url7 = 'https://developers.zomato.com/api/v2.1/collections?city_id='
url7 = base_url7 + city_id + '&count=100'
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
response7 = requests.get(url=url7, headers=header)
data7 = response7.json()
collection_id_list = []
collection_title_list = []
for x in data7['collections']:
    collection_id_list.append(x['collection']['collection_id'])
    collection_title_list.append(x['collection']['title'])
collection_id_and_title_zip = zip(collection_title_list, collection_id_list)
dict_collection_id_and_title = dict(collection_id_and_title_zip )
print(dict_collection_id_and_title)

#get info on restaurants that fall under this category
for x in dict_collection_id_and_title:
    base_url8 = 'https://developers.zomato.com/api/v2.1/search?entity_id='
    url8 = base_url8 + city_id +'&entity_type=city&count=100&collection_id=' + str(x) +'&sort=rating&order=asc'
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
    response8 = requests.get(url=url8, headers=header)
    data8 = response8.json()
    restaurant_id_list = []
    for y in data8['restaurants']:
        #print(x)
        #uprint(y['restaurant'])
        print('\n\n')
        restaurant_id = y['restaurant']['R']['res_id']
        restaurant_id_list.append(restaurant_id)
        restaurant_name = y['restaurant']['name']
        restaurant_address = y['restaurant']['location']['address']
        restaurant_city = y['restaurant']['location']['city']
        restaurant_locality = y['restaurant']['location']['locality_verbose']
        restaurant_lat = y['restaurant']['location']['latitude']
        restaurant_long = y['restaurant']['location']['longitude']
        restaurant_cuisines = y['restaurant']['cuisines']
        avg_cost_2 = y['restaurant']['average_cost_for_two']
        zomato_price_range = y['restaurant']['price_range']
        zomato_rating = y['restaurant']['user_rating']['aggregate_rating']
        zomato_rating_text =  y['restaurant']['user_rating']['rating_text']
#         zomato_rating_votes = y['restaurant']['user_rating']['votes']
#         uprint('restaurant id:', restaurant_id)
#         uprint('restaurant name:', restaurant_name)
#         uprint('adress:', restaurant_address)
#         uprint('locality:', restaurant_locality)
#         uprint('longitude:', restaurant_lat)
#         uprint('lattitude:', restaurant_long)
#         uprint('cuisines:', restaurant_cuisines)
#         uprint('average cost for two: $', avg_cost_2)
#         uprint('zomato price range:', zomato_price_range )
#         uprint('zomato_rating:', zomato_rating)
#         uprint('zomato_rating_text:',zomato_rating_text)
#         uprint('zomato_rating_votes:', zomato_rating_votes)
#         uprint('city:', restaurant_city)
#         print('\n\n')
#
# #get info on restaurant on foursquare
# agree_count_list = []
# text_of_tips_list = []
# tip_text_time_posted_and_agree_counts = {}
# time_created_list = []
# tipper_id_list = []
# tipper_first_name_list = []
# for x in venue_info['response']['venue']['tips']['groups'][0]['items']:
#     text_of_tips_list.append(x['text'])
#     agree_count_list.append(x['agreeCount'])
#     time_created_list.append(x['createdAt'])
#     tipper_id_list.append(x['user']['id'])
#     tipper_first_name_list.append(x['user']['firstName'])
# text__agree_counts_first_id = zip(text_of_tips_list, agree_count_list, time_created_list, tipper_id_list, tipper_first_name_list)
# sorted_text__agree_counts_first_id = sorted(text__agree_counts_first_id, key=operator.itemgetter(1), reverse = True)
# tips_count = venue_info['response']['venue']['tips']['count']
# venue_id = venue_info['response']['venue']['id']
# venue_name = venue_info['response']['venue']['name']
# venue_full_address = str(venue_info['response']['venue']['location']['address'])
# foursqure_rating = venue_info['response']['venue']['rating']
# visits_count = venue_info['response']['venue']['stats']['visitsCount']
# uprint("venue id:", venue_id)
# uprint("venue name:", venue_name)
# uprint("venue_full_address:", venue_full_address)
# uprint("foursqure_rating:", foursqure_rating)
# uprint("visits to restaurant count:", visits_count)
# uprint("text_of_tips_list:",text_of_tips_list)
# uprint("agree_count_list:",agree_count_list)
# uprint("time_created_list:", time_created_list)
# uprint("lat_venue,long_venue:", lat_venue,long_venue)
# uprint("tipper_first_name_list:", tipper_first_name_list)
# uprint("tipper_id_list:", tipper_id_list)
#
# #get time during day, day of week, and date posted
# day = ''
# for a in time_created_list:
#     a1 = time.gmtime(a)
#     if a1[6] == 6:
#         day = 'Sunday'
#     if a1[6] == 5:
#         day = 'Saturday'
#     if a1[6] == 4:
#         day = 'Friday'
#     if a1[6] == 3:
#         day = 'Thursday'
#     if a1[6] == 2:
#         day = 'Wednesday'
#     if a1[6] == 1:
#         day = 'Tuesday'
#     if a1[6] == 0:
#         day = 'Monday'
#     hour_posted = str(a1[3])
#     min_posted = str(a1[4])
#     hour_and_min_1 = hour_posted + ':' + min_posted
#     hour_and_min = datetime.datetime.strptime(hour_and_min_1,'%H:%M').strftime('%I:%M %p')
#     if a1[1] == 1:
#         print(hour_and_min, day,'January', a1[2], a1[0])
#     if a1[1] == 2:
#         print(hour_and_min, day, 'February', a1[2], a1[0])
#     if a1[1] == 3:
#         print(hour_and_min, 'March', a1[2], a1[0])
#     if a1[1] == 4:
#         print(hour_and_min,day, 'April', a1[2], a1[0])
#     if a1[1] == 5:
#         print(hour_and_min,day,'May', a1[2], a1[0])
#     if a1[1] == 6:
#         print(hour_and_min,day, 'June', a1[2], a1[0])
#     if a1[1] == 7:
#         print(hour_and_min,day, 'July', a1[2], a1[0])
#     if a1[1] == 8:
#         print(hour_and_min,day, 'August', a1[2], a1[0])
#     if a1[1] == 9:
#         print(hour_and_min,day, 'September', a1[2], a1[0])
#     if a1[1] == 10:
#         print(hour_and_min,day, 'October', a1[2], a1[0])
#     if a1[1] == 11:
#         print(hour_and_min,day, 'November', a1[2], a1[0])
#     if a1[1] == 12:
#         print(hour_and_min,day, 'December', a1[2], a1[0])
#
# day_list = []
# popular_time_list = []
# days_and_popular_times_dict = {}
# if 'popular' in venue_info.keys():
#     for x in venue_info['response']['venue']['popular']['timeframes']:
#         day_list.append([x][0]['days'])
#         popular_time_list.append([x][0]['open'][0]['renderedTime'])
#         days_and_popular_times_zip_dict = zip(day_list, popular_time_list)
#         days_and_popular_times_dict = dict(days_and_popular_times_zip_dict)
#         uprint("days and thier popular times", days_and_popular_times_dict)
#
# #put lattitude and longitude into format for Google Places API
# lat_long_for_google = str(lat_venue) + ' ' + str(long_venue)
# print('lat_long_for_google:', lat_long_for_google)
#
# #get rating from Google Places API in order to compare it to rating on FourSquare
# base_url3 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
# url3 = base_url3 + 'location=' + lat_long_for_google + '&rankby=distance' + '&type=restaurant' + '&keyword=' + given_place + '&key=' + Keys_and_Secrets.google_places_key
# resp3 = requests.get(url=url3)
# data3 = json.loads(resp3.text)
# uprint('google_price_level:', data3['results'][0]['price_level'])
# google_places_rating = data3['results'][0]['rating']
# uprint('google_places_rating:', google_places_rating)

for y in restaurant_id_list:
    base_url9 = 'https://developers.zomato.com/api/v2.1/reviews?res_id='
    url9 = base_url9 + str(y)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
    #print(url9)
    response = requests.get(url=url9, headers=header)
    data9 = response.json()
    for x in data9['user_reviews']:
        zomato_review_text = x['review']['review_text']
        zomato_review_time_posted = x['review']['timestamp']
        z_reviewer_name = x['user']['name']
        z_reviewer_f_level = x['user']['foodie_level']
        z_reviewer_f_level_num = x['user']['foodie_level_num']
        uprint('zomato review text:', zomato_review_text)
        uprint('zomato review posted:', zomato_review_time_posted)
        uprint('zomato reviewer name:', z_reviewer_f_level)
        uprint('foodie level:', z_reviewer_f_level)
        uprint('foodie level number:', z_reviewer_f_level_num)


# #normalize scores from each API to make it a better comparison
# normalized_foursquare_rating = foursqure_rating / 10
# normalized_google_place_rating = google_places_rating / 5
# normalized_zomato_rating = float(zomato_rating) / 5
# uprint('normalized foursquare rating:' , normalized_foursquare_rating)
# uprint('normalized google places rating:', normalized_google_place_rating)
# uprint('normalized zomato rating', normalized_zomato_rating)
#
# # #creating tables
# # conn = sqlite3.connect('FinalProject.sqlite')
# # cur = conn.cursor()
# # cur.execute("DROP TABLE IF EXISTS Venues")
# # cur.execute("CREATE TABLE Venues (venue_id TEXT, venu_name TEXT)")
# # # #TEXT, venue_name
# # #TEXT, venue_description TEXT, venue_full_address)")
# # tw['response']['vene']['id'],tw['response']['venue']['name']
# #for tw in venue_info:
# #     #tw['response']['venue']['description'], tw['response']['venue']['location']['address']
# #     #cur.execute("INSERT INTO Users (venue_id, venue_name, VALUES (?, ?)", tup)
# #     #venue_description, venue_full_address)
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
