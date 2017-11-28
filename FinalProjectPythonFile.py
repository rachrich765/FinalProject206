## SI 206 2017
## Project 4





import unittest
import itertools
import collections
import json
import sqlite3
import sys
## Your name:Rachel Richardson


#####

##### TWEEPY SETUP CODE:
# Authentication information should be in ..
import requests
from pprint import pprint
my_id = '4WXJB5FPM1JZWXLPM1JXI10JQVUYWXR4ZXTQCP5C4BHP0RCK'
my_secret = 'UNM3JUBSXQJ1QJYIOHNYGWRC2HAPLTNP0GPQX3W023OVXGBO'
url = "https://api.foursquare.com/v2/venues/search"
given_city = input('enter city: ')
params = dict(
  client_id= my_id,
  client_secret= my_secret,
  near= given_city,
  v='20170801',
  limit=1
)
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)
pprint(data)
#get likes, hereNow, popular hours, name
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
# Define your function get_user_tweets here:
# def get_place_info(place):
#     if place in CACHE_DICTION:
#         restaurant_results = CACHE_DICTION[restaurant]
#         else:
#         restaurant_results = api.search()
#         CACHE_DICTION[restaurant] = restaurant_results
#         fw = open(CACHE_FNAME,"w")
#         fw.write(json.dumps(CACHE_DICTION))
#         fw.close()
#     return restaurant_results
