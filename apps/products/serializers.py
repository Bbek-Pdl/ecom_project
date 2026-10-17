from dataclasses import fields

from rest_framework import serializers
from .models import Products
from rest_framework.exceptions import ValidationError


class product_simp_serializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = [
            'id',
            'sku',
            'price',
            'name'
        ]
class product_serializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        exclude = ['created','updated']
        read_only_fields = ['owner','id']

    def update(self, instance, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def validate_sku(self,value):
        if len(value) < 8:
            raise ValidationError("minimun sku lenght is 8")
        return value 
        

    def validate_name(self,value):
        if len(value) < 5:
            raise ValidationError("unsufficient length of name")
        return value
    
    def validate_price(self,value):
        if value < 0:
            raise ValidationError("price cannot be negative")
        return value 
    
    def validate_stock(self,value):
        if value < 0:
            raise ValidationError("stock cannot be negative")
        return value 
        
    def validate_discount(self,value):
        if value < 0 or value > 100:
            raise ValidationError("discount out of range")
        return value 
        
