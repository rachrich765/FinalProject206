## SI 206 2017
## Project 3
## Building on HW7, HW8 (and some previous material!)

##THIS STARTER CODE DOES NOT RUN!!

##OBJECTIVE:
## In this assignment you will be creating database and loading data
## into database.  You will also be performing SQL queries on the data.
## You will be creating a database file: 206_APIsAndDBs.sqlite
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import sys
## Your name:Rachel Richardson
## The names of anyone you worked with on this project: Sarah Jomaa

#####

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
YT_key = 'AIzaSyDq7eNZh7Y-IzWmCUR79bIRsaMYCBCXSCc'

# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON format
api = https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id=4Y4YSpF6d6w&key={YT_key}
##### END TWEEPY SETUP CODE
## Task 1 - Gathering data
## Define a function called get_user_tweets that gets at least 20 Tweets
## from a specific Twitter user's timeline, and uses caching. The function
## should return a Python object representing the data that was retrieved
## from Twitter. (This may sound familiar...) We have provided a
## CACHE_FNAME variable for you for the cache file name, but you must
## write the rest of the code in this file.
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
def get_place_info(place):
    if place in CACHE_DICTION:
        Google_Places_results = CACHE_DICTION[place]
    else:

        Google_Places_results = place.get_rating(place)
        CACHE_DICTION[user] =  Google_Places_results
        fw = open(CACHE_FNAME,"w")
        fw.write(json.dumps(CACHE_DICTION))
        fw.close()
    return Google_Places_results
