
from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



class Register_serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                    min_length = 8,
                                    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm' ]
    def validate(self,data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("password must match ")
        return data

    def validate_username(self,value):
        if len(value) < 3:
            raise ValidationError("username minimun length must be 3")
        return value
    def validate_email(self,value):
        queryset =  self.Meta.model.objects.filter(email__iexact=value)
        if queryset.exists():
            raise ValidationError("email already exists")
        return value

    def create(self, validated_data):
        model = self.Meta.model
        validated_data.pop('password_confirm')
        return model.objects.create_user(**validated_data)


class Users_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =[
            'id',
            'email',
            'username',
        ]
        read_only_fields = ['id','email','username']


class User_profile_serializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = [
            'id',
            'email',
            'username',
        ]
        read_only_fields =['id','email','username']
                              

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length = 8
    )


class Password_change_Serializer(serializers.Serializer):
    old_password = serializers.CharField(
                                        min_length = 8,
                                        )
    new_password = serializers.CharField(
                                        min_length = 8,
                                        )
    new_password_confirm = serializers.CharField(
                                                 min_length = 8,
                                                 )
    


    def validate(self,data):
        if data['new_password'] != data['new_password_confirm']:
            raise ValidationError("password doesnot match ")
        if data['new_password'] == data['old_password']:
            raise ValidationError("match old password ")
        
        return data
    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("password doesnot match ")

        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


    

   

