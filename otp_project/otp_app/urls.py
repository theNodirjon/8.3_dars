from django.urls import path
from . import views

urlpatterns = [
    path('request_otp/', views.request_otp),
    path('verify_otp/', views.verify_otp),
]
