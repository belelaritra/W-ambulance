import json
import geopy
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from requests.structures import CaseInsensitiveDict

import sendmsg as sd
import googleapi

app = Flask(__name__)

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"


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
        msg.body("Hi! I\'m W-Ambulance. \nA Wapp Bot developed by Team: \nLTFT for Innovation-2021")
        responded = True

    if 'sos' in incoming_msg:
        msg.body("Share your current location")
        responded = True

    # Location Message
    if incoming_msg=='' and (latitude != 'None' or longitude != 'None'):
        # Get reverse Data
        #Address, Street_Number, Road, Sublocality1, Sublocality2, District, State, Country, Zipcode = googleapi.reverselocation(latitude, longitude)
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
        Ambulancephoneno = ""
        Ambulancename = ""
        Ambulancelatitude = ""
        Ambulancelongitude = ""
        Ambulanceregno = ""
        Ambulancezipcode = ""

        # Distance Matrix API
        ambulance_address, patient_address, a2pdistance, a2pduration = googleapi.distance2point(Ambulancelatitude,
                                                                                                Ambulancelongitude,
                                                                                                latitude, longitude)
        patient_address, hospital_address, p2hdistance, p2hduration = googleapi.distance2point(latitude,
                                                                                               longitude,
                                                                                               hospital_latitude,
                                                                                               hospital_longitude)

        patientmsg = "Your Ambulance is on its way.\nAmbulance Service Name : " + str(
            Ambulancename) + "\nAmbulance Phone Number : " + str(Ambulancephoneno) + "\nAmbulance Reg. No : " + str(
            Ambulanceregno) + "\nAmbulance Location : " + str(a2pdistance) + " away \nArriving within : " + str(
            a2pduration) + "\n\nHospital Details :\nHospital Name : " + str(
            hospital_name) + "\nHospital Address : " + str(hospital_address) + "\nRating : " + str(
            hospital_rating) + "\nDistance From Your Location : " + str(p2hdistance) + "\nDriving Duration : " + str(
            p2hduration)
        msg.body(patientmsg)
        # Search Ambulance using nearest zipcode & return name,latitude,longitude,zipcode
        ambulancemessage = "Health Emergency!! \nPlease pick up \nName : " + str(profilename) + "\nFrom : " + str(
            Address) + "\nWhatsApp Number : +" + str(whatsappnumber) + "\n\nDestination \nHospital Name : " + str(
            hospital_name) + "\nHospital Address : " + str(hospital_address)

        # Send Ambulance Message
        sd.sendmessage(Ambulancephoneno, ambulancemessage)

        Nearby_Police_Hospital_Number = ""
        Nearby_Police_Hospital_Latitude = ""
        Nearby_Police_Hospital_Longitude = ""
        Nearby_Police_Hospital_Zipcode = ""

        Nearby_Police_Patient_Number = ""
        Nearby_Police_Patient_Latitude = ""
        Nearby_Police_Patient_Longitude = ""
        Nearby_Police_Patient_Zipcode = ""

        # # Send message to police station near to patient
        # police_patientmessage = "Health Emergency!! \nPleace clear the road for Car No : " + str(
        #     Ambulanceregno) + "\nAmbulance Phone No : " + str(Ambulancephoneno) + "\nPatient Address : " + str(
        #     Address) + "\nHospital Name : " + str(hospital_name) + "\nHospital Address : " + str(hospital_address)
        # sd.sendmessage(Nearby_Police_Patient_Number,police_patientmessage)
        #
        # # Send message to police station near to Hospital
        # police_hospitalmessage = "Health Emergency!! \nPleace clear the road for Car No : " + str(
        #     Ambulanceregno) + "\nAmbulance Phone No : " + str(Ambulancephoneno) + "\nPatient Address : " + str(
        #     Address) + "\nHospital Name : " + str(hospital_name) + "\nHospital Address : " + str(hospital_address)
        # sd.sendmessage(Nearby_Police_Hospital_Number, police_hospitalmessage)
        #
        responded = True

    if responded == False:
        msg.body('I am sorry i can only help with quotes!')

    return str(resp)


if __name__ == '__main__':
    app.run()
