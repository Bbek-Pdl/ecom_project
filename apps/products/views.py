import pkgutil
from unicodedata import category

from django.shortcuts import render
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


#  1 search by sku or name 
# filter by category and price range

class list_create_view(ListCreateAPIView):
    serializer_class = product_serializer
    def get_queryset(self):
        
        queryset = Products.objects.all()
        query_params = self.request.query_params
        sku = query_params.get('sku') 
        name =query_params.get('name')
        category = query_params.get('category')
        min_price = query_params.get('min_price')
        max_price = query_params.get('max_price')
        if sku:
            queryset = queryset.filter(sku__iexact = sku)
        
        if name:
            queryset = queryset.filter(name__icontains = name)
        
        if category:
            queryset = queryset.filter(category__icontains = category )
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

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

