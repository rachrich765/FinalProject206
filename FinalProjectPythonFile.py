## SI 206 2017
## Project 4

import operator
import unittest
import itertools
import collections
import json
import sqlite3
import sys
## Your name:Rachel Richardson

import requests
from pprint import pprint

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
#get places rating from FourSquare
my_id_foursquare = '4WXJB5FPM1JZWXLPM1JXI10JQVUYWXR4ZXTQCP5C4BHP0RCK'
my_secret_foursquare = 'UNM3JUBSXQJ1QJYIOHNYGWRC2HAPLTNP0GPQX3W023OVXGBO'
base_url = "https://api.foursquare.com/v2/venues/search?query="
given_place = input('enter place: ')
near_city = input('enter city: ')
params1 = dict(client_id= my_id_foursquare, client_secret= my_secret_foursquare,
 v='20170801', near = near_city, limit=1)
url1 = base_url + given_place + "&intent=browse"
resp1 = requests.get(url=url1, params=params1)
data1 = json.loads(resp1.text)
id_place = data1['response']['venues'][0]['id']
id_place = data1['response']['venues'][0]['id']
uprint(data1['response']['venues'][0])
CACHE_FNAME = "206_FinalProject_cache.json"
## either gets new data or caches data, depending upon what the input
##		to search for is.

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

# # Define your function get_user_tweets here:
def get_place_info(place, city):
    if place in CACHE_DICTION:
        place_results = CACHE_DICTION[place]
    else:
        base_url2 =  'https://api.foursquare.com/v2/venues/'
        url2 = base_url2 + id_place
        params2 = dict(client_id= my_id_foursquare, client_secret= my_secret_foursquare,
         v='20170801', limit = 1)
        data_places = requests.get(url=url2, params=params2)
        place_results = json.loads(data_places.text)
        #uprint(pprint(place_results['response']['venue']['rating']))
        CACHE_DICTION[place] = place_results
        fw = open(CACHE_FNAME,"w")
        fw.write(json.dumps(CACHE_DICTION))
        fw.close()
    return place_results

place_stuff = get_place_info(given_place, near_city)
#print(type(place_stuff))
agree_count_list = []
text_of_reviews_list = []
tip_text_time_posted_and_agree_counts = {}
time_created_list = []

for x in place_stuff['response']['venue']['tips']['groups'][0]['items']:
    text_of_reviews_list.append(x['text'])
    agree_count_list.append(x['agreeCount'])
    time_created_list.append(x['createdAt'])
    text_and_agree_counts = zip(text_of_reviews_list, agree_count_list, time_created_list)
    sorted_text_and_agree_counts = sorted(tip_text_time_posted_and_agree_counts, key=operator.itemgetter(1), reverse = True)
tips_count = place_stuff['response']['venue']['tips']['count']
venue_id = place_stuff['response']['venue']['id']
venue_name = place_stuff['response']['venue']['name']
venue_full_address = str(place_stuff['response']['venue']['location']['address'])
foursqure_rating = place_stuff['response']['venue']['rating']
venue_lat = place_stuff['response']['venue']['location']['lat']
venue_long = place_stuff['response']['venue']['location']['lng']
checkins_count = place_stuff['response']['venue']['stats']['checkinsCount']

day_list = []
popular_time_list = []
days_and_popular_times_dict = {}
for x in place_stuff['response']['venue']['popular']['timeframes']:
    day_list.append([x][0]['days'])
    popular_time_list.append([x][0]['open'][0]['renderedTime'])
days_and_popular_times_dict = zip(day_list, popular_time_list)
days_and_popular_times_dict = dict(days_and_popular_times_dict)

uprint(venue_id)
uprint(venue_name)
uprint(venue_full_address)
uprint(foursqure_rating)
uprint(text_of_reviews_list)
uprint(checkins_count)
uprint(agree_count_list)
uprint(time_created_list)#
# #creating tables
# conn = sqlite3.connect('FinalProject.sqlite')
# cur = conn.cursor()
# cur.execute("DROP TABLE IF EXISTS Places")
# cur.execute("CREATE TABLE Places (place_id TEXT, name TEXT, description TEXT, location TEXT)")
#
# # for tw in place_stuff:
# #     print(tw)
#     #tup = tw['response']['venue']['id'], tw['response']['venue']['name'], tw['response']['venue']['description'], tw['response']['venue']['location']['city']
#     #cur.execute("INSERT INTO Users (place_id, name, description, location) VALUES (?, ?, ?, ?)", tup)
# conn.commit()
# conn = sqlite3.connect('206_APIsAndDBs.sqlite')
# cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS Reviews')
# cur.execute("CREATE TABLE Reviews (name TEXT, rating NUMBER, review TEXT, agreements NUMBER)")
# # # for tw in place_stuff:
# # #     tup = tw['response']['venue']['name']
# # #sorted_text_and_agree_counts[0], tw['response']['venue']['rating'], tw['response']['venue']['tips']['groups'][0]['items'][0]['agreeCount']
# # #     cur.execute("INSERT INTO Tweets (name, review, user_posted, agreements) VALUES (?, ?, ?, ?)", tup)
# conn.commit()
# cur.execute('DROP TABLE IF EXISTS Popularity')
# cur.execute("CREATE TABLE Popularity (name TEXT, popular_hours NUMBER, here_now NUMBER)")
#for tw in place_stuff:
#     tup = tw['response']['venue']['popular'], tw['response']['venue']['hereNow']['count'], tw['response']['venue']['name']
# #     cur.execute("INSERT INTO Tweets (name, here_now, popular_hours) VALUES (?, ?, ?)", tup)
# #
#get lattitude and longitude for data in cache so that Google Places API may be used
google_geocoding_api_key = 'AIzaSyDGFEb0ZfWRf0VdLPJ5NEk_7Rv8gfXJMfw'
url3 = 'https://maps.googleapis.com/maps/api/geocode/json?'
params3 = dict(key = google_geocoding_api_key, address =  '2207 N Clybourn Ave Chicago IL 60614')
resp3 = requests.get(url=url3, params=params3)
data3 = json.loads(resp3.text)
lat_address = str(data3['results'][0]['geometry']['location']['lat'])
long_address = str(data3['results'][0]['geometry']['location']['lng'])
uprint(lat_address, long_address)
# #get rating from Google Places API in order to compare it to rating on FourSquare
google_places_key = 'AIzaSyB5lhcP3c953-H5wnwuel5o8cS33MFLMFE'
url4 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
params4= dict(key= google_places_key, location = '41.921931 -87.66430749999999', rankby = 'distance', keyword = given_place, page_token = 1)
resp4 = requests.get(url=url4, params=params4)
data4 = json.loads(resp4.text)
google_places_rating = data4['results'][0]['rating']
uprint(google_places_rating)
#(lat_address,long_address)

#normalize scores from both sites to make it a better comparison
normalized_foursquare_rating = foursqure_rating / 10
normalized_google_place_rating = google_places_rating / 5
uprint(normalized_foursquare_rating, normalized_google_place_rating)
