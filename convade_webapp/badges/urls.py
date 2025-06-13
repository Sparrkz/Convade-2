from django.urls import path
from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.BadgeListView.as_view(), name='list'),
    path('<int:pk>/', views.BadgeDetailView.as_view(), name='detail'),
    path('my-badges/', views.MyBadgesView.as_view(), name='my_badges'),
    path('create/', views.BadgeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.BadgeUpdateView.as_view(), name='edit'),
] 