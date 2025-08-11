from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from courses.models import HomeCourse
from .forms import ContactForm
import json


def home(request):
    courses = HomeCourse.objects.all()
    """Home page view with contact form"""
    contact_form = ContactForm()
    return render(request, 'base/home.html', {'contact_form': contact_form, 'courses': courses})


@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission"""
    if request.content_type == 'application/json':
        # Handle AJAX request
        try:
            data = json.loads(request.body)
            form = ContactForm(data)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
    else:
        # Handle regular form submission
        form = ContactForm(request.POST)
    
    if form.is_valid():
        # Send email
        if form.send_email():
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.'
                })
            else:
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('home')
        else:
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Sorry, there was an error sending your message. Please try again later.'
                })
            else:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
                return redirect('home')
    else:
        # Form validation errors
        errors = []
        for field, error_list in form.errors.items():
            for error in error_list:
                errors.append(f"{field.title()}: {error}")
        
        if request.content_type == 'application/json':
            return JsonResponse({
                'success': False,
                'message': 'Please correct the following errors: ' + '; '.join(errors),
                'errors': form.errors
            })
        else:
            for error in errors:
                messages.error(request, error)
            return redirect('/')

from django.shortcuts import render
from django.views.generic import TemplateView

class About(TemplateView):
    template_name = 'base/about.html'