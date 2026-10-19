
from django.shortcuts import render
import django_filters
from .models import Products
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from .serializers import ( product_serializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import Products_filter


#  1 search by sku or name 
# filter by category and price range

class list_create_view(ListCreateAPIView):
    serializer_class = product_serializer
    queryset = Products.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = Products_filter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
class retrieve_update_destroy_view(RetrieveUpdateDestroyAPIView):
    serializer_class = product_serializer

    queryset = Products.objects.all()    
    def get_permissions(self):
            if self.request.method in ['PUT','PATCH','DELETE']:
                return [IsAdminUser()]
            return [IsAuthenticated()]
    lookup_field = 'pk'

