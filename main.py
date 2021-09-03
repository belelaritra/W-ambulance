import json
import requests
import pandas
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from requests.structures import CaseInsensitiveDict
from pytz import timezone
from datetime import datetime

# ========== From File
import sendmsg as sd
import googleapi

app = Flask(__name__)

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

# === Date (dd-mm-yyyy) & previous message
previouswappmsg = ""
d1 = datetime.now(timezone("Asia/Kolkata")).strftime("%d-%m-%Y")

@app.route('/', methods=['POST'])
def mybot():
    # ===================== Complete request data
    print(request.form)
    # ===================== received || sent || delivered
    Sms_Status = request.form.get("SmsStatus")

    # ===================== Only work when sms is received
    if Sms_Status == 'received':
        global previouswappmsg
        # ===================== Patient Name
        profilename = request.form.get("ProfileName")
        # ===================== Patient Whatsapp Number
        whatsappnumber = request.form.get("WaId")
        # ===================== patient Message
        message = request.form.get("Body")
        # ===================== Patient Location
        latitude = request.form.get("Latitude")
        longitude = request.form.get("Longitude")

        # ================== Location other than current location
        Location_Address = request.form.get("Address")
        Location_Name = request.form.get("Label")

        print(profilename)
        print(whatsappnumber)

        # ====================== For Simple message
        if message != '':
            print(message)

        # ================== For Location Message
        if latitude != 'None' or longitude != 'None':
            print(latitude, longitude)

        # ================ For Location other than Current Location
        if Location_Name:
            print(Location_Name)
            print(Location_Address)

        print(Sms_Status)

        #==============  Incoming Message
        incoming_msg = request.values.get('Body', '').lower()
        resp = MessagingResponse()
        msg = resp.message()
        responded = False

        # ============== If Message contains hi word
        if 'hi' in incoming_msg:
            msg.body("Hi! 👋 \nI\'m *W-Ambulance* 🚑 \nA Wapp-Bot 🤖 developed by Team : *LTFT*")
            responded = True

        # ============== If Message contains sos word
        if 'sos' in incoming_msg:
            previouswappmsg = 'sos'
            msg.body("Share your *Current Location* 📍")
            responded = True

        # =============== If Message contains Vaccine word
        if 'vaccine' in incoming_msg:
            previouswappmsg = 'vaccine'
            msg.body("For nearest Vaccination centre, 💉 \nShare your *Current Location* 📍")
            responded = True

        # ============= If Previous Message was: SOS & currnt Message is : Current Location
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

            # ======================================== Searches for Nearest Ambulance using Latitude from ambulance.csv
            adf = pandas.read_csv('ambulance.csv')
            ambdata = adf.iloc[(adf['latitude'] - float(hospital_latitude)).abs().argmin()]
            Ambulancename = ambdata['ambulance']
            #ambulanceno1 = nearestdata2['mobileno']
            Ambulancelatitude = ambdata['latitude']
            Ambulancelongitude = ambdata['longitude']
            Ambulancezipcode = ambdata['zipcode']
            Ambulancephoneno = ambdata['testno']
            Ambulanceregno = ambdata['carno']
            Ambulanceaddress = ambdata['address']


            # Distance Matrix API
            ambulance_address, patient_address, a2pdistance, a2pduration = googleapi.distance2point(
                Ambulancelatitude,
                Ambulancelongitude,
                latitude, longitude)
            patient_address, hosp_address, p2hdistance, p2hduration = googleapi.distance2point(latitude,
                                                                                               longitude,
                                                                                               hospital_latitude,
                                                                                               hospital_longitude)

            # ==================== Message for Patient (last return)
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

            # ========================== Send Ambulance Details of Patient
            sd.sendmessage(Ambulancephoneno, ambulancemessage)
            # ========================== Send Ambulance Live Location of Patient
            sd.sendmsglocation(Ambulancephoneno, "Location of Patient", latitude, longitude)

            # ========================= Searches for Nearest Police Station to Patient using Latitude from police.csv

            df = pandas.read_csv('police.csv')
            nearestdata1 = df.iloc[(df['latitude'] - float(latitude)).abs().argmin()]
            Nearby_Police_Patient_Name = nearestdata1['Police_Station']
            #policephoneno1 = nearestdata1['number']
            Nearby_Police_Patient_Zipcode=nearestdata1['zipcode']
            Nearby_Police_Patient_Latitude = nearestdata1['latitude']
            Nearby_Police_Patient_Longitude = nearestdata1['longitude']
            # ================================ Temp Number for Testing
            Nearby_Police_Patient_Number = nearestdata1['testingnum']

            # ========================= Searches for Nearest Police Station to Hospital using Latitude from police.csv

            nearestdata2 = df.iloc[(df['latitude'] - float(hospital_latitude)).abs().argmin()]
            Nearby_Police_Hospital_Name = nearestdata2['Police_Station']
            Nearby_Police_Hospital_Zipcode=nearestdata2['zipcode']
            #policephoneno2 = nearestdata2['number']
            Nearby_Police_Hospital_Latitude = nearestdata2['latitude']
            Nearby_Police_Hospital_Longitude = nearestdata2['longitude']
            # ================================ Temp Number for Testing
            Nearby_Police_Hospital_Number = nearestdata2['testingnum2']


            # ====== Send WhatsApp Message to the Police Station Nearest to the Patient
            police_patientmessage = "Health Emergency!! 🚨 \nPleace clear the road for 🚑\n\nAmbulance No : *" + str(
                Ambulanceregno) + "*\nAmbulance Phone No : *" + str(
                Ambulancephoneno) + "*\n\nPatient Address : *" + str(
                Address) + "*\n\nHospital Name : *" + str(hospital_name) + "*\nHospital Address : *" + str(
                hospital_address) + "*"
            sd.sendmessage(Nearby_Police_Patient_Number, police_patientmessage)
            # ====== Send WhatsApp Message to the Police Station Nearest to the Hospital
            sd.sendmessage(Nearby_Police_Hospital_Number, police_patientmessage)

            responded = True

            # ======== If Previous Message was Vaccine & Cueenr Message is : Current Location
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

            # ========= Send Nearest Vaccination Centre Data
            vaccinemsg = "Nearest Vaccination Centre 💉\n\nName : *" + str(vname) + "*\nAddress : *" + str(
                vaddress) + "*\n\n*Avaibility* ❓\nAvailable Slot : *" + str(vslot) + "*\nVaccine Type : *" + str(
                vtype) + "*\nFee : *" + str(vfee) + "*\nDose 1 : *" + str(vdose1) + "* ; Dose 2 : *" + str(vdose2) + "*"
            msg.body(vaccinemsg)

            responded = True

        if responded == False:
            msg.body('Please try with something else keyword')
    # ================ Send The Message
        return str(resp)

    # ====================== If Sms Status id Delivered
    elif Sms_Status == 'delivered':
        previouswappuser = request.form.get("To")

        print(previouswappuser, previouswappmsg)
        resp = MessagingResponse()
        msg = resp.message()
        msg.body('')
        return str(resp)
    else:
        resp = MessagingResponse()
        msg = resp.message()
        msg.body('Try again')
        return str(resp)


if __name__ == '__main__':
    app.run()
