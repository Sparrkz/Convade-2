from django.urls import path
from . import views

urlpatterns = [
    path("pay/", views.initialize_payment, name="initialize_payment"),
    path("callback/", views.payment_callback, name="payment_callback"),
]
