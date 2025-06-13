from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

class CourseAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/courses.html'

class TestAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/tests.html'

class UserAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/users.html'

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/reports.html'
