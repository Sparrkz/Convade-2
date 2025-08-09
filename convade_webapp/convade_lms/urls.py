"""
URL configuration for convade_lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='base/about.html'), name='about'),
    # path('about/', views.About.as_view(), name='about'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('tests/', include('tests.urls')),
    path('badges/', include('badges.urls')),
    path('certifications/', include('certifications.urls')),
    path('analytics/', include('analytics.urls')),
    path('help/', include('helpcenter.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
