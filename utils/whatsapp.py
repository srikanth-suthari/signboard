from twilio.rest import Client
import os

def send_whatsapp_message(to_number, message_body):
    # Set your credentials as environment variables or replace with your actual values
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH_TOKEN')
    from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    to_whatsapp_number = f'whatsapp:{to_number}'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    return message.sid
