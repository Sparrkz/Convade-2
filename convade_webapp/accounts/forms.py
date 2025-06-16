from django import forms
from allauth.account.forms import SignupForm
from .models import User


class CustomSignupForm(SignupForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Instructor'),  # Using 'teacher' to match model but display as 'Instructor'
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='student',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True,
        }),
        label='I want to join as a'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes to existing fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username...'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password...'})

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data['role']
        user.save()
        return user 