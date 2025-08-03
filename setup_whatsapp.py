#!/usr/bin/env python3
"""
Interactive WhatsApp Configuration Setup for S&M Urban Services
This script helps you configure Twilio WhatsApp integration.
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 WhatsApp Configuration Setup for S&M Urban Services")
    print("=" * 60)
    print()
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("❌ Setup cancelled.")
            return
    
    print("📋 To get your Twilio credentials:")
    print("1. Go to https://www.twilio.com")
    print("2. Sign up for a free account")
    print("3. Find your credentials on the dashboard")
    print()
    
    print("📱 WhatsApp Setup Options:")
    print("1. Sandbox (Free testing) - Use +14155238886")
    print("2. WhatsApp Business API (Production) - Your own number")
    print()
    
    # Get setup type
    setup_type = input("Choose setup type (1 for Sandbox, 2 for Business API): ").strip()
    
    # Get credentials
    print("\n🔐 Enter your Twilio credentials:")
    
    account_sid = input("Account SID (starts with AC...): ").strip()
    if not account_sid.startswith('AC'):
        print("⚠️  Warning: Account SID should start with 'AC'")
    
    auth_token = input("Auth Token: ").strip()
    
    if setup_type == "1":
        from_number = "whatsapp:+14155238886"
        print(f"✅ Using sandbox number: {from_number}")
        print("\n📱 To use sandbox:")
        print("1. Send 'join <sandbox-keyword>' to +1 415 523 8886 from WhatsApp")
        print("2. Check your Twilio console for the exact keyword")
    else:
        from_number = input("Your WhatsApp Business number (e.g., whatsapp:+919876543210): ").strip()
        if not from_number.startswith('whatsapp:'):
            from_number = f"whatsapp:{from_number}"
    
    # Create .env file content
    env_content = f"""# Twilio WhatsApp Configuration for S&M Urban Services
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_WHATSAPP_FROM={from_number}

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database (if using PostgreSQL or MySQL)
# DATABASE_URL=your-database-url-here
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"\n✅ .env file created successfully!")
        
        # Add to .gitignore
        gitignore_file = Path('.gitignore')
        if gitignore_file.exists():
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
            if '.env' not in gitignore_content:
                with open('.gitignore', 'a') as f:
                    f.write('\n.env\n')
                print("📝 Added .env to .gitignore")
        else:
            with open('.gitignore', 'w') as f:
                f.write('.env\n')
            print("📝 Created .gitignore and added .env")
        
        print("\n🧪 Test your configuration:")
        print("python manage.py test_whatsapp")
        print("python manage.py test_whatsapp --test-number +919876543210")
        
        print("\n🔒 Security reminders:")
        print("- Never commit .env file to version control")
        print("- Keep your Auth Token secret")
        print("- Rotate credentials periodically")
        
        print("\n💰 Pricing info:")
        if setup_type == "1":
            print("- Sandbox: Free for testing")
            print("- Limited to verified phone numbers")
        else:
            print("- WhatsApp messages: ~$0.005 - $0.05 per message")
            print("- Free trial includes $15 USD credit")
        
        print("\n✅ Setup complete! Your WhatsApp integration is ready to use.")
        
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return
    
    # Test configuration
    test_now = input("\nDo you want to test the configuration now? (y/n): ").lower()
    if test_now == 'y':
        print("\n🧪 Testing configuration...")
        try:
            # Load environment variables
            if env_file.exists():
                with open('.env', 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value
            
            from utils.whatsapp import check_whatsapp_config
            config = check_whatsapp_config()
            
            if config['configured']:
                print("✅ Configuration is valid!")
                test_number = input("Enter a phone number to send test message (+919876543210): ").strip()
                if test_number:
                    print(f"📱 Sending test message to {test_number}...")
                    from utils.whatsapp import send_whatsapp_message
                    try:
                        message_sid = send_whatsapp_message(
                            test_number,
                            "🧪 Test message from S&M Urban Services!\n\nWhatsApp integration is working! 🎉"
                        )
                        print(f"✅ Message sent successfully! SID: {message_sid}")
                    except Exception as e:
                        print(f"❌ Failed to send message: {e}")
            else:
                print("❌ Configuration issues:")
                for issue in config['issues']:
                    print(f"  - {issue}")
                    
        except ImportError:
            print("⚠️  Run this from your Django project directory")
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
