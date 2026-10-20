from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import (GenericAPIView ,
                                      ListCreateAPIView ,
                                         ListAPIView , 
                                         RetrieveUpdateDestroyAPIView,
                                        CreateAPIView ,
                                        UpdateAPIView,
                                        DestroyAPIView)
from rest_framework.permissions import IsAuthenticated

# Create your views here.

from .models import Cart_item , Cart
from .serializers import (carditem_modify,
                          cart_item_Add,
                          Cart_view_serializer,
                          cart_delete)

class list_cart(ListAPIView):
    serializer_class = Cart_view_serializer
    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related("items__products")

class cart_create(CreateAPIView):
    serializer_class = cart_item_Add
    permission_classes = [IsAuthenticated]

    

class cart_modify_view(UpdateAPIView):
    serializer_class = carditem_modify
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Cart_item.objects.filter(user=self.request.user).select_related("cart", "products")

    

class Cart_items_delete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = cart_delete
    def get_queryset(self):
        return Cart_item.objects.filter(
            cart__user=self.request.user
        )
    