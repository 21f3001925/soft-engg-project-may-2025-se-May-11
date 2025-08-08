# sms_sender.py
from twilio.rest import Client


def send_sms(to_number, message):
    account_sid = "AC97a057c08ebfdfe80ca08c3754bc19b5"
    auth_token = "0c92dcc66dc6fb83912107f066abb466"
    from_number = "+17655655889"  # Your Twilio number

    client = Client(account_sid, auth_token)
    client.messages.create(to=to_number, from_=from_number, body=message)
