from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Jhon Doe',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'jhon@domain.com',
            'required': True
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Write about your enquiry',
            'required': True
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write Your Message',
            'rows': 5,
            'required': True
        })
    )

    def send_email(self):
        """Send email using the form data"""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        # Format the email content
        email_subject = f"Contact Form: {subject}"
        email_body = f"""
New contact form submission from Convade website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the Convade contact form.
        """
        
        try:
            # Send email to admin
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Send to configured email
                fail_silently=False,
            )
            
            # Send confirmation email to user
            confirmation_subject = "Thank you for contacting Convade"
            confirmation_message = f"""
Hello {name},

Thank you for reaching out to us! We have received your message and will get back to you as soon as possible.

Your message:
Subject: {subject}
Message: {message}

Best regards,
The Convade Team
            """
            
            send_mail(
                subject=confirmation_subject,
                message=confirmation_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,  # Don't fail if user email fails
            )
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
