from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('<int:pk>/enroll/', views.EnrollView.as_view(), name='enroll'),
    path('<int:pk>/enroll/confirm/', views.EnrollConfirmView.as_view(), name='enroll_confirm'),
    path('<int:pk>/enroll/success/', views.EnrollSuccessView.as_view(), name='enroll_success'),
    path('<int:pk>/payment/', views.PaymentMethodSelectView.as_view(), name='payment'),
    path('<int:pk>/payment/paystack/', views.PaystackInitView.as_view(), name='paystack_init'),
    path('<int:pk>/payment/flutterwave/', views.FlutterwaveInitView.as_view(), name='flutterwave_init'),
    path('<int:pk>/payment/confirmed/', views.PaymentConfirmedView.as_view(), name='payment_confirmed'),
    path('<int:pk>/content/', views.CourseContentView.as_view(), name='content'),
    path('my-courses/', views.MyCourseListView.as_view(), name='my_courses'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    
    path('api/search/', views.course_search_api, name='search_api'),
    path('api/<int:pk>/progress/', views.update_progress, name='update_progress'),
] 