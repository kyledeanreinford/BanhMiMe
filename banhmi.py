from flask import Flask, render_template
import requests
import geocoder
import json 
from os import environ


app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def home():
    location = geocoder.ip('me').latlng
    my_lat = location[0]
    my_lon = location[1]

    API_KEY = environ.get('API_KEY')
    ENDPOINT = "https://api.yelp.com/v3/businesses/search"
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

    PARAMETERS = {'term': 'banh mi',
                  'limit': 10,
                  'radius': 10000,
                  'offset': 0,
                  'sort_by': 'distance',
                  'latitude': my_lat,
                  'longitude': my_lon,
    }
    response = requests.get(url= ENDPOINT, params= PARAMETERS, headers= HEADERS)

    business_data = response.json()
    biz_dict = []

    for biz in business_data['businesses']:
        if biz['is_closed'] == False:
            biz_dict.append({'name':biz['name'], 'address':biz['location'], 'rating':biz['rating']})
    print (biz_dict, my_lat, my_lon)
    list_of_biz = biz_dict[0:5]
    print(list_of_biz)
    return render_template('home.html', list_of_biz=list_of_biz)

@app.route('/why')
def why():
    return render_template('why.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
