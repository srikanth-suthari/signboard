from twilio.rest import Client
import os
import logging

logger = logging.getLogger(__name__)

def send_whatsapp_message(to_number, message_body):
    """
    Send WhatsApp message using Twilio API
    
    Args:
        to_number (str): Phone number in international format (e.g., +919876543210)
        message_body (str): Message content
        
    Returns:
        str: Message SID if successful, None if failed
    """
    try:
        # Get credentials from environment variables
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        # Check if credentials are properly configured
        if not account_sid or account_sid == 'YOUR_TWILIO_ACCOUNT_SID':
            logger.warning("Twilio Account SID not configured. WhatsApp message not sent.")
            raise Exception("Twilio credentials not configured. Please set TWILIO_ACCOUNT_SID environment variable.")
        
        if not auth_token or auth_token == 'YOUR_TWILIO_AUTH_TOKEN':
            logger.warning("Twilio Auth Token not configured. WhatsApp message not sent.")
            raise Exception("Twilio credentials not configured. Please set TWILIO_AUTH_TOKEN environment variable.")
        
        # Format the recipient number for WhatsApp
        to_whatsapp_number = f'whatsapp:{to_number}'
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        
        logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")
        return message.sid
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {str(e)}")
        raise e

def check_whatsapp_config():
    """
    Check if WhatsApp configuration is properly set up
    
    Returns:
        dict: Configuration status
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    
    config_status = {
        'configured': True,
        'issues': [],
        'account_sid_set': bool(account_sid and account_sid != 'YOUR_TWILIO_ACCOUNT_SID'),
        'auth_token_set': bool(auth_token and auth_token != 'YOUR_TWILIO_AUTH_TOKEN'),
        'from_number': from_number
    }
    
    if not config_status['account_sid_set']:
        config_status['issues'].append('TWILIO_ACCOUNT_SID not configured')
        config_status['configured'] = False
    
    if not config_status['auth_token_set']:
        config_status['issues'].append('TWILIO_AUTH_TOKEN not configured')
        config_status['configured'] = False
    
    return config_status
