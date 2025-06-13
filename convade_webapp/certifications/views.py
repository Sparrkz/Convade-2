from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
