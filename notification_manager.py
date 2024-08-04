import smtplib
import os
from twilio.rest import Client


MY_EMAIL="manhaas1820@gmail.com"
MY_EMAIL_PASSWORD="Soni@1820"
class NotificationManager:

    def __init__(self):

        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        self.twilio_virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number = os.environ["TWILIO_VERIFIED_NUMBER"]
        self.whatsapp_number = os.environ["TWILIO_WHATSAPP_NUMBER"]

        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])
        self.connection = smtplib.SMTP_SSL(self.smtp_address,465)

    def send_sms(self, message_body):

        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )

        print(message.sid)


    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{self.twilio_verified_number}'
        )
        print(message.sid)

    def send_emails(self, email_list, email_body):
        try:
            with smtplib.SMTP_SSL(self.smtp_address, 465) as connection:
                connection.login(self.email, self.email_password)
                for email in email_list:
                    connection.sendmail(
                        from_addr=self.email,
                        to_addrs=email,
                        msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                    )
                print("Emails sent successfully!")
        except smtplib.SMTPException as e:
            print(f"An SMTP error occurred: {e}")
