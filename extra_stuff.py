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
