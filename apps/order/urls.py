from django.urls import path , include
from .views import  Cancel_order, Checkout_view,view_order_history , view_retrieve , view_order_all , update_orders



urlpatterns = [
    path('check-out/',Checkout_view.as_view()),
    path('order_history/',view_order_history.as_view()),
    path('view_individual_order/<str:pk>',view_retrieve.as_view()),
    path('order_all',view_order_all.as_view()),
    path('update_order/<str:pk>',update_orders.as_view()),
    path('cancelled/<str:pk>',Cancel_order.as_view())


]