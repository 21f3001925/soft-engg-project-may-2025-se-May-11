import os
from twilio.rest import Client
from flask_mail import Mail, Message


def send_sms(to_number, body):
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


def send_email(app, to_email, subject, body):
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = (
        os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    )
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

    if not all(
        [
            app.config["MAIL_SERVER"],
            app.config["MAIL_USERNAME"],
            app.config["MAIL_PASSWORD"],
            app.config["MAIL_DEFAULT_SENDER"],
        ]
    ):
        print("Mail server credentials not fully set up. Skipping email.")
        return

    mail = Mail(app)
    msg = Message(subject, recipients=[to_email], body=body)
    try:
        with app.app_context():
            mail.send(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
