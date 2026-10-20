

from importlib.abc import ExecutionLoader

from attr import fields

from .models import (Order ,
                     Order_items, Payment)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from apps.products.models import Products



class CheckoutInputSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(
        max_length=150
    )

    payment_method = serializers.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES
    )
    currency = serializers.CharField(max_length=5,
                                     default="NPR")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = [
            "id",
            "product",
            "name",
            "quantity",
            "unit_price",
            "subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        source="order_items",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shipping_address",
            "shipping_fee",
            "total",
            "currency",
            "status",
            "items",
        ]
        read_only_fields = fields


class Order_Checkout_View(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Order 
        fields = [
            'currency',
            'shipping_address',
            'status',
            ]

class order_list_serializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = [
            'created_at',
            'updated_at',
            'user'
        ]

class order_list_all(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class order_item_serializer(serializers.ModelSerializer):

    class Meta:
        model = Order_items
        fields = '__all__'



class Order_Retrieve_view(serializers.ModelSerializer):

    items = order_item_serializer(source='order_items',
                       many=True,
                       read_only=True)
    class Meta:
            model = Order
            fields = [
                'status',
                'id',
                'shipping_fee',
                'total',
                'shipping_address',
                'items'
            ]


class update_serializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']