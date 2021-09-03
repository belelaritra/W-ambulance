import json
import requests

APIKEY = "____________YOUR API KEY_____________"

# =============== Geocoding API
def reverselocation(latitude, longitude):
    URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitude) +","+ str(longitude) + "&key=" + str(
        APIKEY)
    response = requests.get(URL)
    data = response.json()
    # print(response.text)

    # ================   GEO CODE API (LAT, LONG --> ADDDRESS)
    Address = data['results'][0]['formatted_address']
    # Street_Number = data['results'][0]['address_components'][0]['long_name']
    # Road = data['results'][0]['address_components'][1]['long_name']
    # Sublocality1 = data['results'][0]['address_components'][3]['long_name']
    # Sublocality2 = data['results'][0]['address_components'][2]['long_name']
    # District = data['results'][0]['address_components'][4]['long_name']
    # State = data['results'][0]['address_components'][6]['long_name']
    # Country = data['results'][0]['address_components'][7]['long_name']
    #Zipcode = data['results'][0]['address_components'][8]['long_name']
    Zipcode = data['results'][0]['address_components'][7]['long_name']

    #return Address, Street_Number, Road, Sublocality1, Sublocality2, District, State, Country, Zipcode
    return Address,Zipcode

# =============== Places API
def placedetails(latitude, longitude, radius):
    type = "hospital"
    nameexample = "hospital"
    URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(latitude) + "," + str(
        longitude) + "&radius=" + str(radius) + "&types=" + str(type) + "&name=" + str(
        nameexample) + "rating=max" + "&key=" + str(APIKEY)

    response = requests.get(URL)
    data = response.json()
    # print(response.text)

    # ================   PLACES API (LAT, LONG --> ADDDRESS)
    hospital_latitude = data["results"][0]["geometry"]["location"]["lat"]
    hospital_longitude = data["results"][0]["geometry"]["location"]["lng"]
    hospital_name = data["results"][0]["name"]
    hospital_address = data["results"][0]["vicinity"]
    hospital_rating = data["results"][0]["rating"]

    return hospital_latitude, hospital_longitude, hospital_name, hospital_address, hospital_rating

# =============== Distance Matrix API
def distance2point(olatitude, olongitude, dlatitude, dlongitude):
    # ============= DISTANCE MATRIX API (DIST BETWEEN 2 API)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(olatitude) + "," + str(
        olongitude) + "&destinations=" + str(dlatitude) + "," + str(dlongitude) + "&mode=DRIVING&key=" + str(APIKEY)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    # print(response.text)

    destination_address = data["destination_addresses"]
    original_address = data["origin_addresses"]
    distance = data["rows"][0]["elements"][0]["distance"]["text"]
    duration = data["rows"][0]["elements"][0]["duration"]["text"]

    return original_address, destination_address, distance, duration
