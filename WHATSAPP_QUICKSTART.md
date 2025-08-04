# 🚀 Quick WhatsApp Setup Guide

## Current Status
❌ Twilio credentials not configured
✅ WhatsApp code is ready and working

## Quick Setup (5 minutes)

### Step 1: Get Twilio Account (Free)
1. Go to **https://www.twilio.com**
2. Click **"Try Twilio for Free"**
3. Sign up with your email and phone
4. Verify your phone number

### Step 2: Get Your Credentials
After logging in, you'll see on the dashboard:
- **Account SID**: Starts with `AC...` (like `ACa1b2c3d4e5f6...`)
- **Auth Token**: Click the 👁️ eye icon to reveal it

### Step 3: Set Up WhatsApp Sandbox (Free Testing)
1. In Twilio Console → **"Develop"** → **"Messaging"** → **"Try it out"** → **"Send a WhatsApp message"**
2. You'll see instructions like: *"Send 'join <keyword>' to +1 415 523 8886"*
3. Send that message from your WhatsApp to join the sandbox

### Step 4: Configure Your App
Run the setup script:
```bash
python3 setup_whatsapp.py
```

Or manually create `.env` file:
```bash
# .env file
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Step 5: Test It
```bash
python3 manage.py test_whatsapp --test-number +919876543210
```

## Example Credentials (After Setup)
```
Account SID: ACa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Auth Token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
From Number: whatsapp:+14155238886 (sandbox)
```

## What Happens After Setup?
✅ Contractors get WhatsApp welcome messages when they register
✅ Contractors get booking notifications when customers book them
✅ Messages include all booking details (customer info, project details, etc.)

## Costs
- **Sandbox**: FREE (for testing)
- **Production**: ~₹0.40 per WhatsApp message
- **Free Trial**: $15 USD credit (~₹1,200 worth of messages)

## Need Help?
1. **Twilio Support**: https://support.twilio.com
2. **Documentation**: https://www.twilio.com/docs/whatsapp
3. **Our Setup Scripts**: Run `python3 setup_whatsapp.py` for interactive setup

## Security Notes
🔒 Never share your Auth Token
🔒 Never commit `.env` file to Git
🔒 The `.env` file is already added to `.gitignore`
