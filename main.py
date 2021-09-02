import json
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from requests.structures import CaseInsensitiveDict

import sendmsg as sd
import googleapi
from pytz import timezone
from datetime import datetime

d1 = datetime.now(timezone("Asia/Kolkata")).strftime("%d-%m-%Y")

app = Flask(__name__)

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

previouswappmsg = ""


# Sms_Status --> received (incoming) --> Longitude
# Sms_Status --> sent then (outgoing) --> To Phone Number
# Sms_Status --> delivered (outgoing) --> To Phone Number

@app.route('/', methods=['POST'])
def mybot():
    # Complete request data
    print(request.form)
    # received || sent || delivered
    Sms_Status = request.form.get("SmsStatus")

    # Only work when sms is received
    if Sms_Status == 'received':
        global previouswappmsg
        # Patient Name
        profilename = request.form.get("ProfileName")
        # Patient Whatsapp Number
        whatsappnumber = request.form.get("WaId")
        # patient Message
        message = request.form.get("Body")
        # Patient Location
        latitude = request.form.get("Latitude")
        longitude = request.form.get("Longitude")

        # Location other than current location
        Location_Address = request.form.get("Address")
        Location_Name = request.form.get("Label")

        print(profilename)
        print(whatsappnumber)

        # For Simple message
        if message != '':
            print(message)

        # For Location Message
        if latitude != 'None' or longitude != 'None':
            print(latitude, longitude)

        # For Location other than Current Location
        if Location_Name:
            print(Location_Name)
            print(Location_Address)

        print(Sms_Status)

        # Incoming Message
        incoming_msg = request.values.get('Body', '').lower()
        resp = MessagingResponse()
        msg = resp.message()
        responded = False

        if 'hi' in incoming_msg:
            msg.body("Hi! 👋 \nI\'m *W-Ambulance* 🚑 \nA Wapp-Bot 🤖 developed by Team : *LTFT*")
            responded = True

        if 'sos' in incoming_msg:
            previouswappmsg = 'sos'
            msg.body("Share your *Current Location* 📍")
            responded = True

        if 'vaccine' in incoming_msg:
            previouswappmsg = 'vaccine'
            msg.body("For nearest Vaccination centre, 💉 \nShare your *Current Location* 📍")
            responded = True

        if ((previouswappmsg == 'sos') & (latitude != None)):
            previouswappmsg = "soslocation"
            # Get reverse Data
            # Address, Street_Number, Road, Sublocality1, Sublocality2, District, State, Country, Zipcode = googleapi.reverselocation(latitude, longitude)
            Address, Zipcode = googleapi.reverselocation(latitude, longitude)
            print(Address)

            # Searches nearby Hospital (latitude, longitude, radius in meter)
            hospital_latitude, hospital_longitude, hospital_name, hospital_address, hospital_rating = googleapi.placedetails(
                latitude, longitude, 5000)

            print(hospital_name)
            print(hospital_address)
            print(hospital_latitude)
            print(hospital_longitude)
            # From CSV file
            Ambulancephoneno = "6290960905"
            Ambulancename = "AMBULANCE TEST"
            Ambulancelatitude = "22.59374327026721"
            Ambulancelongitude = "88.32434306693492"
            Ambulanceregno = "WB12A1234"
            Ambulancezipcode = "711101"

            # Distance Matrix API
            ambulance_address, patient_address, a2pdistance, a2pduration = googleapi.distance2point(
                Ambulancelatitude,
                Ambulancelongitude,
                latitude, longitude)
            patient_address, hosp_address, p2hdistance, p2hduration = googleapi.distance2point(latitude,
                                                                                                   longitude,
                                                                                                   hospital_latitude,
                                                                                                   hospital_longitude)

            patientmsg = "Your Ambulance is on its way. 🚑\nAmbulance Service Name : *" + str(
                Ambulancename) + "*\nAmbulance Phone Number : *" + str(
                Ambulancephoneno) + "*\nAmbulance Reg. No : *" + str(
                Ambulanceregno) + "*\nAmbulance Location : *" + str(
                a2pdistance) + "* away \nArriving within : *" + str(
                a2pduration) + "*\n\n*Hospital Details* 🏥\nHospital Name : *" + str(
                hospital_name) + "*\nHospital Address : *" + str(hospital_address) + "*\nRating : *" + str(
                hospital_rating) + "*⭐️\nDistance From Your Location : *" + str(
                p2hdistance) + "*\nDriving Duration : *" + str(
                p2hduration) + "*"
            msg.body(patientmsg)

            # Search Ambulance using nearest zipcode & return name,latitude,longitude,zipcode
            ambulancemessage = "Health Emergency!! \nPlease pick up \nName : " + str(profilename) + "\nFrom : " + str(
                Address) + "\nWhatsApp Number : +" + str(whatsappnumber) + "\n\nDestination \nHospital Name : " + str(
                hospital_name) + "\nHospital Address : " + str(hospital_address)

            # Send Ambulance Message
            sd.sendmessage(Ambulancephoneno, ambulancemessage)
            sd.sendmsglocation(Ambulancephoneno,"Location of Patient", latitude, longitude)

            Nearby_Police_Hospital_Number = "9062184542"
            Nearby_Police_Hospital_Latitude = "22.570257802949584"
            Nearby_Police_Hospital_Longitude = "88.3573208336781"
            Nearby_Police_Hospital_Zipcode = "700012"

            Nearby_Police_Patient_Number = "7439872575"
            Nearby_Police_Patient_Latitude = "22.592230984825406"
            Nearby_Police_Patient_Longitude = "88.32060692445842"
            Nearby_Police_Patient_Zipcode = "711101"
            #
            # # Send message to police station near to patient
            police_patientmessage = "Health Emergency!! 🚨 \nPleace clear the road for 🚑\n\nAmbulance No : *" + str(
            Ambulanceregno) + "*\nAmbulance Phone No : *" + str(Ambulancephoneno) + "*\n\nPatient Address : *" + str(
            Address) + "*\n\nHospital Name : *" + str(hospital_name) + "*\nHospital Address : *" + str(hospital_address) + "*"
            sd.sendmessage(Nearby_Police_Patient_Number,police_patientmessage)

            sd.sendmessage(Nearby_Police_Hospital_Number, police_patientmessage)

            responded = True
        if ((previouswappmsg == 'vaccine') & (latitude != None)):
            previouswappmsg = "vaccinelocation"
            Address, Zipcode = googleapi.reverselocation(latitude, longitude)
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + str(
                Zipcode) + "&date=" + str(d1)

            response = requests.get(url)
            data = response.json()
            vname = data['sessions'][0]['name']
            vaddress = data['sessions'][0]['address']
            vfee = data['sessions'][0]['fee']
            vdose1 = data['sessions'][0]['available_capacity_dose1']
            vdose2 = data['sessions'][0]['available_capacity_dose2']
            vtype = data['sessions'][0]['vaccine']
            vslot = data['sessions'][0]['slots'][0]

            vaccinemsg = "Nearest Vaccination Centre 💉\n\nName : *" + str(vname) + "*\nAddress : *" + str(
                vaddress) + "*\n\n*Avaibility* ❓\nAvailable Slot : *" + str(vslot) + "*\nVaccine Type : *" + str(
                vtype) + "*\nFee : *" + str(vfee) + "*\nDose 1 : *" + str(vdose1) + "* ; Dose 2 : *" + str(vdose2) + "*"
            msg.body(vaccinemsg)
            responded = True

        if responded == False:
            msg.body('Please try with something else keyword')

        return str(resp)
    elif Sms_Status == 'delivered':
        previouswappuser = request.form.get("To")

        print(previouswappuser, previouswappmsg)


if __name__ == '__main__':
    app.run()
