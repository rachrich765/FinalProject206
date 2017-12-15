## SI 206 2017
## Project 4
# Your name:Rachel Richardson
import json
import sqlite3
import sys
import requests
import Keys_and_Secrets
import time

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

#zomato_api_key = ""
#google_places_key = ""
city = 'chicago'

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
    CACHE_DICTION1 = dict()

#either get city info from cache or get it by connecting to the Zomato API
def get_zomato_city(city):
    if city in CACHE_DICTION1:
        city_results = CACHE_DICTION1[city]
    else:
        base_url6 = 'https://developers.zomato.com/api/v2.1/cities?q='
        url6 = base_url6 + city
        header6 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response6 = requests.get(url=url6, headers=header6)
        data6 = response6.json()
        city_results = data6
        CACHE_DICTION1[city] = city_results
        fw = open(CACHE_FNAME1,"w")
        fw.write(json.dumps(CACHE_DICTION1))
        fw.close()
    return city_results

#get Zomato city id for chicago
city_info = get_zomato_city(city)
zomato_city_id = str(city_info['location_suggestions'][0]['id'])
uprint(city, "zoatmo city id:", zomato_city_id)

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
    CACHE_DICTION3 = dict()

#get info on restaurants in
#"trending this week" collection for given city, either from cache
#or from Zomato API
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

#get "Trending This Week Collection"
# after reading the documentation, I noted that it is collection #1
collection = str(1)

#call function to get which restaurants are in this collection in the city of Chicago
restaurants_info = get_zomato_restaurants_in_collection(collection)

zomato_restaurant_id_list = list()
zomato_restaurant_name_list =list()
restaurant_address_list = list()
restaurant_locality_list = list()
restaurant_cuisine_list = list()
zomato_review_text_list = list()
zomato_rating_text_list = list()
zomato_rating_list = list()
zomato_rating_votes_list = list()
zomato_price_range_list = list()
avg_cost_2_list = list()
dict_names_and_ids = dict()
dict_names_and_addresses = dict()
dict_names_and_localities = dict()
dict_names_and_lat_long = dict()
dict_name_and_rating = dict()
dict_name_and_price_rating = dict()
dict_name_and_rating_text = dict()
dict_rating_text_and_votes = dict()
dict_name_and_avg_cost2 = dict()

#get specified info from each of the 30 restaurants in the collection
for y in restaurants_info['restaurants']:
    zomato_restaurant_id = str(y['restaurant']['R']['res_id'])
    zomato_restaurant_id_list.append(zomato_restaurant_id)
    zomato_restaurant_name = y['restaurant']['name']
    zomato_restaurant_name_list.append(zomato_restaurant_name)
    dict_names_and_ids[zomato_restaurant_name] = zomato_restaurant_id
    restaurant_address = y['restaurant']['location']['address']
    restaurant_address_list.append(restaurant_address)
    dict_names_and_addresses[zomato_restaurant_name] = restaurant_address
    restaurant_locality = y['restaurant']['location']['locality_verbose']
    restaurant_locality_list.append(restaurant_locality)
    dict_names_and_localities[zomato_restaurant_name] = restaurant_locality
    restaurant_lat = y['restaurant']['location']['latitude']
    restaurant_long = y['restaurant']['location']['longitude']
    lat_and_long = str(restaurant_lat) + "" + str(restaurant_long)
    dict_names_and_lat_long[zomato_restaurant_name] = lat_and_long
    zomato_price_range = y['restaurant']['price_range']
    zomato_price_range_list.append(zomato_price_range)
    dict_name_and_price_rating[zomato_restaurant_name] = zomato_price_range
    zomato_rating = y['restaurant']['user_rating']['aggregate_rating']
    zomato_rating_list.append(zomato_rating)
    dict_name_and_rating[zomato_restaurant_name] = zomato_rating
    zomato_rating_text =  y['restaurant']['user_rating']['rating_text']
    zomato_rating_text_list.append(zomato_rating_text)
    dict_name_and_rating_text[zomato_restaurant_name] = zomato_rating_text
    zomato_rating_votes = y['restaurant']['user_rating']['votes']
    zomato_rating_votes_list.append(zomato_rating_votes)
    dict_rating_text_and_votes[zomato_rating_text] = zomato_rating_votes
    avg_cost_2 = y['restaurant']['average_cost_for_two']
    avg_cost_2_list.append(avg_cost_2)
    dict_name_and_avg_cost2[zomato_restaurant_name] = avg_cost_2
uprint('dictionary of restaurant names and ids:', dict_names_and_ids)
uprint('dictionary of restaurant names and addresses:', dict_names_and_addresses)
uprint('dictionary of restaurant names and localities:', dict_names_and_localities)
uprint('dictionary of restaurant names and their lattitudes and longitudes:', dict_names_and_lat_long)
uprint('dictionary of restaurant names and thier ratings:', dict_name_and_rating)
uprint("dictonary of restaurant names and their price ratings:", dict_name_and_price_rating)
uprint('dictionary of restuarant names and the text of the ratings:', dict_name_and_rating_text)


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
    CACHE_DICTION4 = dict()

#get restaurant reviews for 30 restaurants, either from the cache
#or from Zomato API
def get_zomato_restaurant_reviews(restaurant_id1):
    if restaurant_id1 in CACHE_DICTION4:
        review_results = CACHE_DICTION4[restaurant_id1]
    else:
        base_url9 = 'https://developers.zomato.com/api/v2.1/reviews?res_id='
        url9 = base_url9 + restaurant_id1 + '&count=1'
        header9 = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": Keys_and_Secrets.zomato_api_key}
        response9 = requests.get(url=url9, headers=header9)
        data9 = response9.json()
        review_results = data9
        CACHE_DICTION4[restaurant_id1] = review_results
        fw = open(CACHE_FNAME4,"w")
        fw.write(json.dumps(CACHE_DICTION4))
        fw.close()
    return review_results

zomato_reviewer_name_list = []
zomato_review_text_list = []
zomato_reviewer_foodie_level_word_list = []
zomato_reviewer_foodie_level_number_list = []
zomato_time_review_posted_list = []
dict_restaurant_id_and_review_text = dict()
dict_review_and_reviewer_name = dict()
dict_reviewer_name_and_foodie_level_word = dict()

#get detailed information on one review for each of the 30 restaurants
for y in zomato_restaurant_id_list:
    restaurant_reviews = get_zomato_restaurant_reviews(y)
    zomato_review_text = restaurant_reviews['user_reviews'][0]['review']['review_text']
    zomato_review_text_list.append(zomato_review_text)
    dict_restaurant_id_and_review_text[y] = zomato_review_text
    zomato_review_time_posted1 = restaurant_reviews['user_reviews'][0]['review']['timestamp']
    zomato_time_review_posted_list.append(zomato_review_time_posted1)
    z_reviewer_name = restaurant_reviews['user_reviews'][0]['review']['user']['name']
    zomato_reviewer_name_list.append(z_reviewer_name)
    z_reviewer_f_level = restaurant_reviews['user_reviews'][0]['review']['user']['foodie_level']
    zomato_reviewer_foodie_level_word_list.append(z_reviewer_f_level)
    dict_reviewer_name_and_foodie_level_word[z_reviewer_name] =  z_reviewer_f_level
    z_reviewer_f_level_num = restaurant_reviews['user_reviews'][0]['review']['user']['foodie_level_num']
    zomato_reviewer_foodie_level_number_list.append(z_reviewer_f_level_num)

#convert timestamp to day, month, year, hour:min:sec format
zomato_time_review_posted_list2 = []
for f in zomato_time_review_posted_list:
    f1 = time.gmtime(f)
    zomato_review_time_posted2 = time.strftime("%c", f1)
    zomato_time_review_posted_list2.append(zomato_review_time_posted2)


CACHE_FNAME6 = "google_restaurants_cache.json"
# # # either gets new data or caches data, depending upon what the input
# # #		to search for is.
cache_file6 = open(CACHE_FNAME6, 'r')
try:
    cache_contents6 = cache_file6.read()
    CACHE_DICTION6 = json.loads(cache_contents6)
    cache_file6.close()
except:
    CACHE_DICTION6 = dict()

#using lattitude and longitude information from Zomato API, get restaurant info
#either from cache or from Google API
def get_google_restaurant_info(google_restaurant):
    if google_restaurant in CACHE_DICTION6:
        google_restaurant_results = CACHE_DICTION6[google_restaurant]
    else:
        #make sure only returns results of restaurants
        base_url3 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        url3 = base_url3 + 'location=' + lat_and_long + '&type=restaurant' + '&rankby=distance&keyword=' + ab + '&key=' + Keys_and_Secrets._key
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
google_places_names_list = []
dict_google_names_and_ratings = {}
dict_google_names_and_price_levels = dict()

# #get details on price level and rating for restaurants obtained from Zomato
for ab in zomato_restaurant_name_list:
    google_restaurant_info = get_google_restaurant_info(ab)
    #only get restaurants for which there is information provided for them
    if len(google_restaurant_info['results']) == 0:
        continue
    else:
        #only get restaurants that have price and rating information
        # so that it is easier to compare between Zomato and Google
        if "rating" in google_restaurant_info['results'][0] and "price_level" in google_restaurant_info['results'][0]:
            google_places_rating = google_restaurant_info['results'][0]['rating']
            google_places_rating_list.append(google_places_rating)
            google_places_name = google_restaurant_info['results'][0]['name']
            dict_google_names_and_ratings[google_places_name] = google_places_rating
            google_places_names_list.append(google_places_name)
            google_price_level = google_restaurant_info['results'][0]['price_level']
            google_price_level_list.append(google_price_level)
            dict_google_names_and_price_levels[google_places_name] = google_price_level
uprint("dictionary of restaurant names and ratings according to Google:", dict_google_names_and_ratings)
uprint("dictionary of restaurant names and price levels according to Google:", dict_google_names_and_price_levels)

#creat zip items to iterate over when creating tables in database
zip_general_restaurant_info = zip(zomato_restaurant_name_list, restaurant_address_list, restaurant_locality_list, restaurant_cuisine_list)
zip_interactions_zomato_part_1 = zip(zomato_restaurant_name_list, zomato_rating_list, avg_cost_2_list, zomato_price_range_list)
zip_interactions_google = zip(google_places_names_list, google_places_rating_list, google_price_level_list)
zip_interactions_zomato_part_2 = zip(zomato_restaurant_name_list, zomato_review_text_list, zomato_time_review_posted_list2, zomato_reviewer_name_list, zomato_reviewer_foodie_level_word_list, zomato_reviewer_foodie_level_number_list)


# creating database

#creating first table

#connect to database
conn = sqlite3.connect('FinalProject.sqlite')
#create cursor
cur = conn.cursor()
#remove the table added with the CREATE TABLE statement (if it exists)
cur.execute("DROP TABLE IF EXISTS General_Restaurant_Info")
#create table with given labels (row titles)
cur.execute("CREATE TABLE General_Restaurant_Info (restaurant_name TEXT, restaurant_address TEXT, restaurant_locality TEXT, restaurant_cuisines TEXT)")
#create tuples from zip object containing general restaurant info
for y in zip_general_restaurant_info:
    tup = y[0], y[1], y[2], y[3]
#insert general restaurant info into table as tuples
    cur.execute("INSERT INTO General_Restaurant_Info (restaurant_name, restaurant_address, restaurant_locality, restaurant_cuisines) VALUES (?, ?, ?, ?)", tup)
conn.commit()
cur.close()

#creating second table

#connect to database
conn = sqlite3.connect('FinalProject.sqlite')
#create cursor
cur = conn.cursor()
#remove the table added with the CREATE TABLE statement (if it exists)
cur.execute('DROP TABLE IF EXISTS Zomato_Interactions_Part_1')
#create table with given lables (row titles)
cur.execute("CREATE TABLE Zomato_Interactions_Part_1 (restaurant_name TEXT, zomato_rating_out_of_5 NUMBER,average_cost_for_two NUMBER, zomato_price_range_out_of_5 NUMBER)")
#create tuples from zip object containing first part of Zomato ineractions per restaurant
for y in zip_interactions_zomato_part_1:
    tup = y[0], y[1], y[2], y[3]
    #insert first part of Zomato interactions into table as tuples
    cur.execute("INSERT INTO Zomato_Interactions_Part_1 (restaurant_name, zomato_rating_out_of_5,average_cost_for_two, zomato_price_range_out_of_5) VALUES (?, ?, ?, ?)", tup)
conn.commit()
cur.close()

#creating third table

#connect to database
conn = sqlite3.connect('FinalProject.sqlite')
#create cursor
cur = conn.cursor()
#remove the table added with the CREATE TABLE statement (if it exists)
cur.execute('DROP TABLE IF EXISTS Interactions_Part_2_Zomato_Reviews')
#create table with given lables (row titles)
cur.execute("CREATE TABLE Interactions_Part_2_Zomato_Reviews (restaurant_name TEXT, zomato_review_text TEXT, zomato_time_review_posted TEXT, zomato_reviewer_name TEXT, zomato_reviewer_foodie_level_word TEXT,zomato_reviewer_foodie_level_number TEXT)")
#create tuples from zip object containing details on Zomato reviews for each restaurant
for y in zip_interactions_zomato_part_2:
    tup = y[0], y[1], y[2], y[3], y[4], y[5]
    #insert details on Zomato Reviews into table as tuples
    cur.execute("INSERT INTO Interactions_Part_2_Zomato_Reviews (restaurant_name, zomato_review_text, zomato_time_review_posted, zomato_reviewer_name, zomato_reviewer_foodie_level_word,zomato_reviewer_foodie_level_number) VALUES (?, ?, ?, ?, ?, ?)", tup)
conn.commit()
cur.close()

#creating fourth tables

#connect to database
conn = sqlite3.connect('FinalProject.sqlite')
#create cursor
cur = conn.cursor()
#remove the table added with the CREATE TABLE statement (if it exists)
cur.execute('DROP TABLE IF EXISTS Google_Interactions')
#create table with given lables (row titles)
cur.execute("CREATE TABLE Google_Interactions (restaurant_name TEXT, google_rating_out_of_5 NUMBER, google_price_range_out_of_5 NUMBER)")
#create tuples from zip object containing details on interactions on Google for each restaurant
for y in zip_interactions_google:
    tup = y[0], y[1], y[2]
        #insert details on Google interactions into table as tupels
    cur.execute("INSERT INTO Google_Interactions (restaurant_name, google_rating_out_of_5, google_price_range_out_of_5) VALUES (?, ?, ?)", tup)
conn.commit()
cur.close()
