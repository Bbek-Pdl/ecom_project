from django.shortcuts import render
from .models import (Order,
                    Order_items,
                    Products)
from .serializers import (Order_Checkout_View,
                          OrderSerializer,
                          order_list_serializer,
                          Order_Retrieve_view,
                          order_list_all,
                          update_serializer)
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.generics import (GenericAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     )
from .service import checkout ,Cancelled
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class Checkout_view(CreateAPIView):
    serializer_class = Order_Checkout_View
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = checkout(user=user,data=serializer.validated_data)

        order_serializer = OrderSerializer(order)

        headers = self.get_success_headers(order_serializer.data)
        
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class view_order_history(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = order_list_serializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class view_retrieve(RetrieveAPIView):
    serializer_class = Order_Retrieve_view
    
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("order_items")

class view_order_all(ListAPIView):

    permission_classes =[IsAdminUser]
    serializer_class = order_list_all

    def get_queryset(self):
        return Order.objects.select_related("user").all()


class update_orders(UpdateAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = update_serializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Order.objects.all()


class Cancel_order(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order_cancel = Cancelled(user=self.request.user,orderid=order.id)
        serializer = OrderSerializer(order_cancel)
        return Response(serializer.data,status=status.HTTP_200_OK)