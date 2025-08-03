# WhatsApp Integration Setup Guide

## Current Status
✅ Code is implemented and working
❌ Real WhatsApp messages not being sent (using placeholder credentials)

## Setup Options

### Option 1: Twilio WhatsApp API (Recommended for Production)

#### Step 1: Create Twilio Account
1. Go to https://twilio.com
2. Sign up for a free account
3. Verify your phone number

#### Step 2: Get WhatsApp API Access
1. In Twilio Console, go to "Develop" > "Messaging" > "WhatsApp"
2. Apply for WhatsApp Business API approval
3. Note: This requires business verification and can take time

#### Step 3: Get Your Credentials
After approval, you'll get:
- Account SID (starts with AC...)
- Auth Token
- WhatsApp-enabled phone number

#### Step 4: Configure Environment Variables
Create a `.env` file in your project root:

```bash
# .env file
TWILIO_ACCOUNT_SID=your_actual_account_sid_here
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+your_whatsapp_number
```

#### Step 5: Install python-decouple
```bash
pip install python-decouple
```

### Option 2: Twilio Sandbox (For Testing)

#### For immediate testing:
1. Go to Twilio Console > WhatsApp Sandbox
2. Send "join <sandbox-keyword>" to +1 415 523 8886
3. Use sandbox credentials:

```bash
TWILIO_ACCOUNT_SID=your_trial_account_sid
TWILIO_AUTH_TOKEN=your_trial_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Option 3: Alternative WhatsApp API Providers

#### WhatsApp Business API Providers:
- **360Dialog**: Business WhatsApp API
- **Wati**: WhatsApp Business API
- **Gupshup**: Multi-channel messaging
- **Twilio** (as discussed above)

## Current Code Analysis

The application currently:
1. ✅ Sends welcome messages to contractors during registration
2. ✅ Sends booking notifications to contractors when customers book them
3. ✅ Handles errors gracefully (shows success even if WhatsApp fails)
4. ✅ Formats phone numbers correctly (+91 prefix for India)

## Cost Considerations

### Twilio Pricing (approximate):
- WhatsApp messages: $0.005 - $0.05 per message
- SMS fallback: $0.0075 per message
- Free trial: $15 credit for testing

### Free Alternatives for Small Scale:
- **Twilio Sandbox**: Free for testing (limited to verified numbers)
- **Meta WhatsApp Business API**: Direct integration (more complex setup)

## Implementation Status

Current implementation in `utils/whatsapp.py`:
```python
# Currently using placeholder values
account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH_TOKEN')
from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
```

## Next Steps

1. **Immediate Testing**: Set up Twilio sandbox for testing
2. **Production**: Apply for WhatsApp Business API
3. **Configuration**: Set up environment variables
4. **Testing**: Test with real phone numbers

## Security Notes

- Never commit real credentials to version control
- Use environment variables or secure configuration management
- Rotate credentials periodically
- Monitor usage to prevent abuse
