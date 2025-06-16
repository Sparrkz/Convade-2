from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress, EmailConfirmation

User = get_user_model()

class Command(BaseCommand):
    help = 'Test email functionality for Convade LMS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-email',
            type=str,
            default='test@example.com',
            help='Email address to use for testing'
        )
        parser.add_argument(
            '--skip-smtp',
            action='store_true',
            help='Skip SMTP connection test'
        )

    def handle(self, *args, **options):
        test_email = "youngkhito@gmail.com"
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Convade LMS Email Tests\n')
        )
        
        self.print_email_settings()
        self.test_basic_email(test_email)
        self.test_html_email(test_email)
        
        if not options['skip_smtp'] and not settings.DEBUG:
            self.test_smtp_connection()
        
        self.test_email_verification(test_email)
        
        self.stdout.write(
            self.style.SUCCESS('\n✨ Email testing completed!')
        )

    def print_email_settings(self):
        """Print current email settings"""
        self.stdout.write(self.style.WARNING('\n📧 Current Email Settings:'))
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        self.stdout.write(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
        self.stdout.write(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
        self.stdout.write(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")

    def test_basic_email(self, test_email):
        """Test basic email sending"""
        self.stdout.write(self.style.WARNING('\n🧪 Testing basic email sending...'))
        try:
            send_mail(
                'Test Email from Convade LMS',
                'This is a test email to verify email configuration.',
                settings.DEFAULT_FROM_EMAIL,
                [test_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✅ Basic email test successful!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Basic email test failed: {e}')
            )

    def test_html_email(self, test_email):
        """Test HTML email sending"""
        self.stdout.write(self.style.WARNING('\n🧪 Testing HTML email...'))
        try:
            email = EmailMessage(
                subject='Test HTML Email from Convade LMS',
                body='<h1>Test Email</h1><p>This is a <strong>test HTML email</strong> from Convade LMS.</p>',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_email],
            )
            email.content_subtype = 'html'
            email.send()
            self.stdout.write(self.style.SUCCESS('✅ HTML email test successful!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ HTML email test failed: {e}')
            )

    def test_smtp_connection(self):
        """Test SMTP connection without sending email"""
        self.stdout.write(self.style.WARNING('\n🧪 Testing SMTP connection...'))
        try:
            from django.core.mail import get_connection
            connection = get_connection()
            connection.open()
            self.stdout.write(self.style.SUCCESS('✅ SMTP connection successful!'))
            connection.close()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ SMTP connection failed: {e}')
            )

    def test_email_verification(self, test_email):
        """Test allauth email verification"""
        self.stdout.write(self.style.WARNING('\n🧪 Testing email verification...'))
        try:
            # Create a test user if doesn't exist
            user, created = User.objects.get_or_create(
                username='emailtestuser',
                defaults={
                    'email': test_email,
                    'first_name': 'Email',
                    'last_name': 'Test'
                }
            )
            
            # Send verification email
            send_email_confirmation(None, user, signup=True)
            self.stdout.write(self.style.SUCCESS('✅ Email verification test successful!'))
            
            # Show pending confirmations
            confirmations = EmailConfirmation.objects.filter(
                email_address__user=user
            ).count()
            self.stdout.write(f"📧 Pending email confirmations: {confirmations}")
            
            # Clean up test user if we created it
            if created:
                self.stdout.write('🧹 Cleaning up test user...')
                user.delete()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Email verification test failed: {e}')
            ) 