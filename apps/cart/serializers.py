from dataclasses import fields
from decimal import Decimal

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
        
        queryset = Products.objects.filter(id=value.id).first()
        if not queryset:
            raise ValidationError("products doesnot exist")
        
        return value
    def create(self, validated_data):
        user = self.context['request'].user
        cart,created = Cart.objects.get_or_create(user=user)
        if self.Meta.model.objects.filter(cart=cart,products=validated_data['products']).exists():
            raise ValidationError("products already exists")
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

    products = product_simp_serializer(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    class Meta:
            model = Cart_item
            fields =[
                'id',
                'quantity',
                'products',
                'subtotal',
            ]
    
    def get_subtotal(self,obj) -> Decimal:
        return ((obj.products.price  * ( 1 - obj.products.discount/100) ) * obj.quantity)

class Cart_view_serializer(serializers.ModelSerializer):
    user = User_profile_serializer(read_only=True)
    cart_item = cart_item_serializer(source="items",
                                    many=True,
                                    read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = [
            'user',
            'cart_item',
            'total',
            
        ]

    def get_total(self,obj) -> Decimal:
        return sum(
            (item.products.price * (1 -  item.products.discount/100) )* item.quantity
            for item in obj.items.all()
        )
    def validate_cart_item(self,value):
        print(value)



class cart_delete(serializers.ModelSerializer):


    class Meta:
        model = Cart
        fields = ['__all__']