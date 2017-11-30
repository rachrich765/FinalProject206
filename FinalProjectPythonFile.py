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
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
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
text_and_agree_counts = {}
for x in place_stuff['response']['venue']['tips']['groups'][0]['items']:
    text_of_reviews_list.append(x['text'])
    agree_count_list.append(x['agreeCount'])
    text_and_agree_counts = zip(text_of_reviews_list, agree_count_list)
    sorted_text_and_agree_counts = sorted(text_and_agree_counts, key=operator.itemgetter(1), reverse = True)

venue_id = place_stuff['response']['venue']['id']
venue_name = place_stuff['response']['venue']['name']
venue_full_address = str(place_stuff['response']['venue']['location']['formattedAddress'])
rating = place_stuff['response']['venue']['rating']
most_popular_tip = sorted_text_and_agree_counts[0][0]
agree_count_of_most_agreed = sorted_text_and_agree_counts[0][1]
people_there_now = place_stuff['response']['venue']['hereNow']['count']

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
uprint(str(venue_full_address))
uprint(rating)
uprint(most_popular_tip)
uprint(agree_count_of_most_agreed)
uprint(people_there_now)
uprint(days_and_popular_times_dict)
#
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
params3 = dict(key = google_geocoding_api_key, address = venue_full_address)
resp3 = requests.get(url=url3, params=params3)
data3 = json.loads(resp3.text)
lat_address = str(data3['results'][0]['geometry']['location']['lat'])
long_address = str(data3['results'][0]['geometry']['location']['lng'])
uprint(lat_address, long_address)
# #get rating from Google Places API in order to compare it to rating on FourSquare
google_places_key = 'AIzaSyB5lhcP3c953-H5wnwuel5o8cS33MFLMFE'
url4 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
params4= dict(key= google_places_key, location = '41.9428366, -87.64906129999997', rankby = 'distance', keyword = given_place, page_token = 1)
resp4 = requests.get(url=url4, params=params4)
data4 = json.loads(resp4.text)
uprint(data4['results'][0]['rating'])
#(lat_address,long_address)
