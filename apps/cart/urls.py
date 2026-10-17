from django.urls import path , include
from .views import (list_cart , cart_create,cart_modify_view,Cart_items_delete)


urlpatterns = [
    path('list_view_cart/',list_cart.as_view()),
    path('add_in_cart/',cart_create.as_view()),
    path('cart_item_modify/<int:pk>',cart_modify_view.as_view()),
    path('Cart_items_delete/<int:pk>',Cart_items_delete.as_view())
    

]