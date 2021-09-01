import json
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

def decdeg2dms(dd):
   mnt,sec = divmod(dd*3600,60)
   deg,mnt = divmod(mnt,60)
   return deg,mnt,sec

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

@app.route('/', methods=['POST'])
def mybot():
    # Complete request data
    print(request.form)

    # Patient Name
    profilename = request.form.get("ProfileName")

    # Patient Whatsapp Number
    whatsappnumber = request.form.get("WaId")

    # Patiens's Message
    message = request.form.get("Body")

    #Location of Patient (lat,lon)
    latitude = request.form.get("Latitude")
    longitude = request.form.get("Longitude")

    #Location in Deg, Min, Sec format
    latdeg, latmin, latsec = decdeg2dms(float(latitude))
    londeg, lonmin, lonsec = decdeg2dms(float(latitude))

    #Reverse geocoding using API
    url = "https://api.geoapify.com/v1/geocode/reverse?lat=" + str(latitude) + "&lon=" + str(longitude) + "&apiKey=" + "_______YOUR API KEY_______"

    #Request data
    response = requests.get(url, headers=headers)

    #Json data
    data = json.loads(response.text)

    #print(data["features"][0]["properties"])

    # housenumber = data["features"][0]["properties"]["housenumber"]
    # postcode = data["features"][0]["properties"]["postcode"]
    # name = data["features"][0]["properties"]["name"]
    country = data["features"][0]["properties"]["country"]
    city = data["features"][0]["properties"]["city"]
    street = data["features"][0]["properties"]["street"]
    state = data["features"][0]["properties"]["state"]
    address = data["features"][0]["properties"]["formatted"]
    address_line1 = data["features"][0]["properties"]["address_line1"]
    address_line2 = data["features"][0]["properties"]["address_line2"]

    #Address of Patient in Terminal
    print(address)

    #Google Map URL
    #addressurl = "https://www.google.co.in/maps/place/"+str(format(latdeg,".1f"))+"°"+str(format(latmin,".1f"))+"\'"+str(format(latsec,".2f"))+"\""+"+"+str(format(londeg,".1f"))+"°"+str(format(lonmin,".1f"))+"\'"+str(format(lonsec,".2f"))+"/@"+str(latitude)+","+str(longitude)


    resp = MessagingResponse()
    msg = resp.message()
    #s = str(formatted)+"\n"+str(addressurl)

    #Reply message --> Address
    msg.body(address)
    #Reply
    return str(resp)

if __name__ == '__main__':
    app.run()
