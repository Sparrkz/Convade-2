from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('courses/', views.CourseAnalyticsView.as_view(), name='courses'),
    path('tests/', views.TestAnalyticsView.as_view(), name='tests'),
    path('users/', views.UserAnalyticsView.as_view(), name='users'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
] 