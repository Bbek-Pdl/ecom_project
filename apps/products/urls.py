from django.urls import path , include
from .views import (list_create_view ,retrieve_update_destroy_view)
urlpatterns = [
    path('list_create/',list_create_view.as_view()),
    path('retrieve_update_dest/<int:pk>/',retrieve_update_destroy_view.as_view()),
]