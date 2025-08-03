from django.core.management.base import BaseCommand
from utils.whatsapp import check_whatsapp_config, send_whatsapp_message
import os

class Command(BaseCommand):
    help = 'Test WhatsApp configuration and send a test message'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-number',
            type=str,
            help='Phone number to send test message (e.g., +919876543210)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== WhatsApp Configuration Check ===')
        )
        
        # Check configuration
        config = check_whatsapp_config()
        
        if config['configured']:
            self.stdout.write(
                self.style.SUCCESS('✅ WhatsApp is properly configured!')
            )
            self.stdout.write(f"From Number: {config['from_number']}")
        else:
            self.stdout.write(
                self.style.ERROR('❌ WhatsApp configuration issues found:')
            )
            for issue in config['issues']:
                self.stdout.write(f"  - {issue}")
            
            self.stdout.write("\nTo configure WhatsApp:")
            self.stdout.write("1. Set environment variables:")
            self.stdout.write("   export TWILIO_ACCOUNT_SID='your_account_sid'")
            self.stdout.write("   export TWILIO_AUTH_TOKEN='your_auth_token'")
            self.stdout.write("   export TWILIO_WHATSAPP_FROM='whatsapp:+your_number'")
            self.stdout.write("\n2. Or create a .env file with these variables")
            return
        
        # Test message if number provided
        test_number = options.get('test_number')
        if test_number:
            self.stdout.write(f"\nSending test message to {test_number}...")
            try:
                message_sid = send_whatsapp_message(
                    test_number,
                    "🧪 Test message from S&M Urban Services!\n\nIf you received this, WhatsApp integration is working correctly! 🎉"
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Test message sent successfully! Message SID: {message_sid}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send test message: {str(e)}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('\nTo send a test message, use:')
            )
            self.stdout.write('python manage.py test_whatsapp --test-number +919876543210')
        
        self.stdout.write("\n=== Current Environment Variables ===")
        sensitive_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_WHATSAPP_FROM']
        for var in sensitive_vars:
            value = os.environ.get(var, 'Not set')
            if var in ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN'] and value != 'Not set':
                # Mask sensitive values
                masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                self.stdout.write(f"{var}: {masked_value}")
            else:
                self.stdout.write(f"{var}: {value}")
