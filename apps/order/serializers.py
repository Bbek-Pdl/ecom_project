from .models import (Order ,
                     Order_items, Payment)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import Products


class product_serilizer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = []


class Order_Checkout_View(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    Payment = serializers.CharField(read_only=True)
    class Meta:
        model = Order 
        fields = [
            'currency',
            'shipping_address',
            'status',
            'Payment',
            ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)