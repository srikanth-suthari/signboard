#!/bin/bash

# WhatsApp Setup Script for S&M Urban Services
echo "🚀 Setting up WhatsApp Integration for S&M Urban Services"
echo "========================================================="

echo ""
echo "📋 Step 1: Get Twilio Credentials"
echo "1. Go to https://www.twilio.com and sign up"
echo "2. After login, you'll see your credentials on the dashboard:"
echo "   - Account SID (starts with AC...)"
echo "   - Auth Token (click eye icon to reveal)"
echo ""

echo "📱 Step 2: WhatsApp Setup Options"
echo ""
echo "Option A: Sandbox (Free Testing)"
echo "- Go to Twilio Console → Messaging → Try it out → WhatsApp"
echo "- Send 'join <sandbox-keyword>' to +1 415 523 8886"
echo "- Use sandbox number: whatsapp:+14155238886"
echo ""
echo "Option B: WhatsApp Business API (Production)"
echo "- Apply for WhatsApp Business API in Twilio Console"
echo "- Get your own WhatsApp business number"
echo ""

echo "🔧 Step 3: Configure Environment Variables"
echo "Create a .env file in your project root with:"
echo ""
echo "# For Sandbox Testing:"
echo "TWILIO_ACCOUNT_SID=your_account_sid_here"
echo "TWILIO_AUTH_TOKEN=your_auth_token_here"
echo "TWILIO_WHATSAPP_FROM=whatsapp:+14155238886"
echo ""
echo "# For Production (after getting WhatsApp Business API):"
echo "TWILIO_ACCOUNT_SID=your_account_sid_here"
echo "TWILIO_AUTH_TOKEN=your_auth_token_here"
echo "TWILIO_WHATSAPP_FROM=whatsapp:+your_whatsapp_business_number"
echo ""

echo "💰 Step 4: Pricing Information"
echo "- Twilio Free Trial: $15 USD credit"
echo "- WhatsApp messages: ~$0.005 - $0.05 per message"
echo "- Sandbox: Free (limited to verified numbers)"
echo ""

echo "🧪 Step 5: Test Your Setup"
echo "After configuring, test with:"
echo "python manage.py test_whatsapp --test-number +919876543210"
echo ""

echo "📞 Need Help?"
echo "- Twilio Support: https://support.twilio.com"
echo "- Documentation: https://www.twilio.com/docs/whatsapp"
echo ""

# Prompt for credentials if user wants to set them now
read -p "Do you want to set up credentials now? (y/n): " setup_now

if [ "$setup_now" = "y" ] || [ "$setup_now" = "Y" ]; then
    echo ""
    echo "🔐 Enter your Twilio credentials:"
    read -p "Account SID (starts with AC...): " account_sid
    read -s -p "Auth Token: " auth_token
    echo ""
    read -p "WhatsApp From Number (e.g., whatsapp:+14155238886): " from_number
    
    # Create .env file
    cat > .env << EOF
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=$account_sid
TWILIO_AUTH_TOKEN=$auth_token
TWILIO_WHATSAPP_FROM=$from_number

# Add other environment variables as needed
DEBUG=True
SECRET_KEY=your-secret-key-here
EOF
    
    echo ""
    echo "✅ .env file created successfully!"
    echo "🔒 Important: Never commit .env file to version control"
    echo ""
    
    # Add .env to .gitignore if it doesn't exist
    if ! grep -q ".env" .gitignore 2>/dev/null; then
        echo ".env" >> .gitignore
        echo "📝 Added .env to .gitignore"
    fi
    
    echo ""
    echo "🧪 You can now test with:"
    echo "python manage.py test_whatsapp --test-number +919876543210"
fi

echo ""
echo "✅ Setup guide complete!"
echo "📖 For detailed instructions, see WHATSAPP_SETUP.md"
