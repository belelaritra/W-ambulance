# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "_____YOUR ACCOUNT SID_____"
auth_token = "_____YOUR ACCOUNT AUTH TOKEN_____"
client = Client(account_sid, auth_token)


def sendmessage(to,msg):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=str(msg),
        status_callback='http://postb.in/1234abcd',
        to='whatsapp:+91'+str(to)
    )
    print(message.Status)

def sendmsglocation(to,msg,latitude,longitude):
    message = client.messages \
        .create(
        from_='whatsapp:+14155238886',
        body=str(msg),
        persistent_action=['geo:'+str(latitude)+','+str(longitude)],
        to='whatsapp:+91'+str(to)
    )
    print(message.Status)

