import os

# Lazily import Twilio client to avoid failing app startup when package is not installed.
try:
    from twilio.rest import Client
except Exception:
    Client = None


def send_whatsapp_message(to_number, message_body):
    """Send a WhatsApp message via Twilio.

    If the Twilio client is not available (package not installed), this function
    will no-op and return None so development checks/servers can run.
    """
    if Client is None:
        # Twilio not installed; skip sending in development and return None
        return None

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
