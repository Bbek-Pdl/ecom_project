from django.db import models
from apps.products.models import Products
from apps.user.models import User
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='cart')
    

class Cart_item(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name="items")
    products = models.ForeignKey(Products,
                                 on_delete=models.CASCADE,
                                 related_name="cart_item")
    quantity = models.IntegerField(default=0   ,
                                    blank=False,
                                    null=False,
                                    verbose_name="cart_quantity")
    
    added_at = models.DateTimeField(auto_now_add=True)    
    
    
