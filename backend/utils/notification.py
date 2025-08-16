import os
from twilio.rest import Client
from flask_mail import Message
from extensions import mail


def send_sms(to_number, body):
    # Generate your twilio free trial credentials and put here to test

    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")

    if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
        print("Twilio credentials not fully set up. Skipping SMS.")
        return

    client = Client(twilio_account_sid, twilio_auth_token)
    try:
        message = client.messages.create(
            to=to_number, from_=twilio_phone_number, body=body
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


def send_email(app, recipient, subject, body):

    try:
        msg = Message(
            subject,
            sender=app.config.get("MAIL_DEFAULT_SENDER"),
            recipients=[recipient],
        )
        msg.body = body
        mail.send(msg)
        print(f"Successfully sent email to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")
        return False
