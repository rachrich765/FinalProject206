import FinalProjectPythonFile
import plotly
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='RACHJR36', api_key='em0Xg7tMTqZkYXaCwB9D')

split_x_list = []
spring_list = []
summer_list = []
fall_list = []
winter_list = []

#separate reviews posted by month, then append the months that
#correspond to each season to the respective list
for x in FinalProjectPythonFile.zomato_time_review_posted_list2:
    split_x = x.split()
    split_x_list.append(split_x)
for y in split_x_list:
    if y[1] == 'Mar':
        spring_list.append(y[1])
    if  y[1] == 'Apr':
        spring_list.append(y[1])
    if  y[1] =='May':
        spring_list.append(y[1])
    if y[1] == 'Jun':
        summer_list.append(y[1])
    if y[1] == 'Jul':
        summer_list.append(y[1])
    if y[1] == 'Aug':
        summer_list.append(y[1])
    if y[1] == 'Sep':
        fall_list.append(y[1])
    if y[1] == "Oct":
        fall_list.append(y[1])
    if y[1] == 'Nov':
        fall_list.append(y[1])
    if y[1] == "Dec":
        winter_list.append(y[1])
    if y[1] == "Jan":
        winter_list.append(y[1])
    if y[1] == "Feb":
            winter_list.append(y[1])

#create pie chart
fig = {
  "data": [
    {
      "values": [len(spring_list), len(summer_list), len(fall_list), len(winter_list)],
      "labels": ['Spring','Summer','Fall','Winter'],
      "hoverinfo":"label+percent",
      'marker': {'colors': ['rgb(60,179,113)',
                                  'rgb(255,215,0)',
                                  'rgb(205,92,92)',
                                  'rgb(255,250,250)']},
      "hole": 0.0,
      "type": "pie"
    }],
  "layout": {
        "title":"Zomato Reviews Posted per Season for Restaurants Trending in Chicago this Week"
}
}
plotly.offline.plot(fig, filename='Ratings per season.html')
#
#
#

for i in range(len(FinalProjectPythonFile.google_places_names_list)):
    if FinalProjectPythonFile.google_places_names_list[i] == 'Mindy\u2019s HotChocolate':
        FinalProjectPythonFile.google_places_names_list[i] = 'Mindy\'s' + " " + 'Hot Chocolate'
    if FinalProjectPythonFile.google_places_names_list[i] == 'Carson\'s' + " " +  "Prime Steaks & Famous Barbecue":
        FinalProjectPythonFile.google_places_names_list[i] = 'Carson\'s' + " " + "Ribs"
for i in range(len(FinalProjectPythonFile.zomato_restaurant_name_list)):
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Ara On':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = "AraOn Restaurant"
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Chicago Q':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = 'Chicago q, Barbecue Restaurant Down Town , Gold Coast Best BBQ'
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'The Berghoff':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = 'The Berghoff Restaurant'
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Uncle Julio\'s':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] ='Uncle Julio\'s' + " " + 'Fine Mexican Food'
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Fabulous Freddies':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = 'Fabulous Freddies Italian Eatery'
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Nico Osteria - Thomson Hotels Chicago':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = 'Nico Osteria'
    if FinalProjectPythonFile.zomato_restaurant_name_list[i] == 'Tavern on Rush':
        FinalProjectPythonFile.zomato_restaurant_name_list[i] = 'Tavern On Rush'


zomato_rating_and_name_zip = zip(FinalProjectPythonFile.zomato_restaurant_name_list,FinalProjectPythonFile.zomato_rating_list)
zomato_rating_and_name_dict  = dict(zomato_rating_and_name_zip)
google_rating_and_name_zip = zip(FinalProjectPythonFile.google_places_names_list, FinalProjectPythonFile.google_places_rating_list)
google_rating_and_name_dict = dict(google_rating_and_name_zip)
google_rating_list_updated = []
zomato_rating_list_updated = []
names_list = []

#match up names only found in Google dictionary with respective ratings
#(either from Zomato or Google API)
for k in google_rating_and_name_dict:
    google_rating_list_updated.append(google_rating_and_name_dict[k])
    zomato_rating_list_updated.append(zomato_rating_and_name_dict[k])
    names_list.append(k)

#create side-by-side bar chart
trace3 = go.Bar(x = [y for y in names_list], y = [z for z in zomato_rating_list_updated], name = 'Zomato Rating', marker = dict(color = 'rgb(255,0,0)')) #red to correspond with Zomato logo / site colors
trace4 = go.Bar(x = [y for y in names_list], y = [z for z in google_rating_list_updated], name = 'Google Rating',  marker = dict(color = 'rgb(50,205,50)')) #green for Google
data = [trace3, trace4]
layout = go.Layout(
     barmode='group',
     title = 'Google Ratings vs. Zomato Ratings for Restaurants Trending in Chicago this Week',
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='GoogleVsZomato.html')
