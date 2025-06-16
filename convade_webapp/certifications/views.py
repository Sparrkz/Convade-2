from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Certificate

# Create your views here.

class CertificateListView(ListView):
    template_name = 'certifications/list.html'

class CertificateDetailView(DetailView):
    template_name = 'certifications/detail.html'

class CertificateDownloadView(LoginRequiredMixin, TemplateView):
    template_name = 'certifications/download.html'

class CertificateVerifyView(TemplateView):
    template_name = 'certifications/verify.html'

class MyCertificatesView(LoginRequiredMixin, TemplateView):
    template_name = 'certifications/my_certificates.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's certificates
        certificates = Certificate.objects.filter(
            student=user
        ).select_related('course', 'course__instructor').order_by('-issued_at')
        
        # Separate by status
        issued_certificates = certificates.filter(status='issued')
        pending_certificates = certificates.filter(status='pending')
        
        context.update({
            'certificates': certificates,
            'issued_certificates': issued_certificates,
            'pending_certificates': pending_certificates,
            'total_certificates': certificates.count(),
            'issued_count': issued_certificates.count(),
            'pending_count': pending_certificates.count(),
        })
        
        return context
