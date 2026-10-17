from dataclasses import fields

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import Products
from .models import Cart_item ,Cart
from apps.products.serializers import product_simp_serializer
from apps.user.serializers import User_profile_serializer


class cart_item_Add(serializers.ModelSerializer):

    class Meta:
        model = Cart_item
        fields = [
            'products',
            'quantity'
        ]
    def validate_products(self,value):
        queryset = Products.object.filter(id=value).first()
        if not queryset:
            raise ValidationError("products doesnot exist")
        
        # if not queryset.active:
        #     raise ValidationError("the produt is not active cann't added")
        
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.filter(user=user)
        if not cart:
            cart = Cart.objects.create(user)
        validated_data['cart'] =cart
         
        return super().create(validated_data)


class carditem_modify(serializers.ModelSerializer):

    class Meta:
        model = Cart_item
        fields = [
            'products',
            'quantity'
        ]
    def validate_quantity(self,value):
        if value < 0:
            raise ValidationError("quantity cannot be negative")
        return value
    
        
    


class cart_item_serializer(serializers.ModelSerializer):

    product = product_simp_serializer(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    class Meta:
            model = Cart_item
            fields =[
                'quantity',
                'products'
                'subtotal'
            ]
    
    def get_subtotal(self,obj):
        return obj.product.price * obj.quantity

class Cart_view_serializer(serializers.ModelSerializer):
    user = User_profile_serializer(read_only=True)
    cart_item = cart_item_serializer(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = [
            'user'
            'cart_item',
            'total',
        ]

    def get_total(self,obj):
        return sum(
            item.product.price * item.quantity
            for item in obj.cart_item
        )
