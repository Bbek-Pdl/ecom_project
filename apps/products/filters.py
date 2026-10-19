from os import name
from .models import Category , Products

import django_filters
from .models import Products

class Products_filter(django_filters.FilterSet):
    sku = django_filters.CharFilter(
        field_name='sku',
        lookup_expr='iexact'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='Category__slug',
        lookup_expr='iexact'
    )
    minprice = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    maxprice = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )

    class Meta:
        model = Products
        fields = [
            'sku',
            'name',
            'category',
            'minprice',
            'maxprice'
        ]