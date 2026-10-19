from django.urls import path , include
from .views import Checkout_view



urlpatterns = [
    path('check-out/',Checkout_view.as_view()),
]