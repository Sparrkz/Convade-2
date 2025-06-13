from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('', views.CertificateListView.as_view(), name='list'),
    path('<int:pk>/', views.CertificateDetailView.as_view(), name='detail'),
    path('<int:pk>/download/', views.CertificateDownloadView.as_view(), name='download'),
    path('verify/<str:verification_code>/', views.CertificateVerifyView.as_view(), name='verify'),
    path('my-certificates/', views.MyCertificatesView.as_view(), name='my_certificates'),
] 