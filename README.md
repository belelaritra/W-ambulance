# W-ambulance-

In Terminal Run:<br>
`pip install twilio`<br>
`pip install Flask`<br>
`pip install requests`<br>

<br>For Twilio click [here](www.twilio.com/referral/Njt8YO)
<br>
> Login / Create Account using Email & Mobile number
>> Click on: Develop -> Messaging -> Try it out -> Send a WhatsApp message
>>> Send your activation code (eg. join ....) to +14155238886 


<br>For GEOAPI click [here](https://myprojects.geoapify.com/login)
>Login using Google
>>Create a `project`
>>>Click on --> `Billing` & Select --> `Free Plans`
>>>>Click on --> `Api Keys` & Copy --> `API KEYS`
>>>>>Change that API KEY with `_______YOUR API KEY_______` ( `Line: 40` in `main.py`file )

<br>Download `ngrok` from [here](https://ngrok.com/download)<br>
>Unzip the file
>>open `terminal` from `Downloads` or where you have saved that file
>>>paste `./ngrok http 5000` inside your terminal & press enter
>>>>Copy --> Forwarding No.1 (eg. http://..........ngrok.io) --> & Paste that [here](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Fsandbox%3Fx-target-region%3Dus1) [When A Message Comes In Box]
>>>>>Copy --> Forwarding No.2 (eg. http://..........ngrok.io) --> & Paste that [here](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Fsandbox%3Fx-target-region%3Dus1) [Status Callback URL]
