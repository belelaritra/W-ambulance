# W-ambulance
A Whatsapp Bot developed by Team : LTFT ([Aritra](https://github.com/belelaritra),[Rounak](https://github.com/CoderRounak),[Mayukh](https://github.com/mayukh551), [Abesh](https://github.com/Abesh1903)) for Hackathon (Innovision-2021 by Department of CSE RCCIIT)\

### Flow Chart
<img src="https://github.com/belelaritra/W-ambulance/blob/main/Wambulance.png" width="700"/>

## Inspiration : 
According to NIEM almost 20 % of patients are died due to traffic delays, & in year 2016 only 1.4 lakh people died in road accident out of which almost 30% died due to late arrival of Ambulance. 
So we team LTFT comes with this idea to build a **WhatsApp Bot** which will help a user to contact an Ambulance, Hospital & nearby Police Station in no time.

As in emergency it's quite to search for an ambulance , hospital in google or to install new health related apps from PlayStore/Appstore. As nowadays almost everyone have a Whatsapp account, so we thought to build a WhatsApp Bot.

## What it does: 
>It asks a WhatsApp user to share his/her 'current location' and according to that it searches for nearby Ambulance & shares that patient's complete details (with live location)  to the nearest Ambulance. 
>>And then it searches for nearest hospital (with highest rating in google) within a given radius & shares that data with the ambulance & patient as destination (with distance & estimate driving time) in a single WhatsApp message.
>>>And then it searches for nearest police station to the Hospital & Patient and asks both of them to clear road jam between Ambulance Location - Patient Location & Patient Location - Hospital Location , and shares ambulance's complete details (eg. Number Plate Details) with pick up & drop off location.

Also, it shares nearest vaccination centres details according to your location through WhatsApp.

## How we built it : 
We built it using `Flask`, `Twilio`, `Google Reverse Geocoding API`, `Google Places API`, `Google Distance Matrix API` & to read csv dataset we have used `pandas`

## User Manual
`pip install twilio`<br>
`pip install Flask`<br>
`pip install requests`<br>

<br>For Twilio click [here](www.twilio.com/referral/Njt8YO)
<br>
> Login / Create Account using Email & Mobile number
>> Click on: Develop -> Messaging -> Try it out -> Send a WhatsApp message
>>> Send your activation code (eg. join ....) to +14155238886 


<br>For Google API click [here](https://console.cloud.google.com/apis/dashboard)
>Login using Google
>>Create a `project`
>>>Create --> `Billing Account` --> Wait for Verification
>>>>Search --> `Geocoding API` --> Enable it ---> Copy --> `API KEY`
>>>>>Search --> `Places API` --> Enable it ---> Copy --> `API KEY`
>>>>>Search --> `Distance MAtrix API` --> Enable it ---> Copy --> `API KEY`

<br>Download `ngrok` from [here](https://ngrok.com/download)<br>
>Unzip the file
>>open `terminal` from `Downloads` or where you have saved that file
>>>paste `./ngrok http 5000` inside your terminal & press enter
>>>>Copy --> Forwarding No.1 (eg. http://..........ngrok.io) --> & Paste that [here](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Fsandbox%3Fx-target-region%3Dus1) [When A Message Comes In Box]
>>>>>Copy --> Forwarding No.2 (eg. http://..........ngrok.io) --> & Paste that [here](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Fsandbox%3Fx-target-region%3Dus1) [Status Callback URL]
