from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('<int:pk>/enroll/', views.EnrollView.as_view(), name='enroll'),
    path('<int:pk>/content/', views.CourseContentView.as_view(), name='content'),
    path('my-courses/', views.MyCourseListView.as_view(), name='my_courses'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    
    path('api/search/', views.course_search_api, name='search_api'),
    path('api/<int:pk>/progress/', views.update_progress, name='update_progress'),
] 