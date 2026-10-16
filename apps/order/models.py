from django.db import models
from apps.user.models import User
import uuid
from apps.products.models import Products
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled")
]
    status = models.CharField(max_length=20,
                             choices=STATUS_CHOICES,
                             verbose_name="status",
                             default="pending")
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             related_name="orders")
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        ) 
    shipping_fee = models.DecimalField(max_digits=12,
                                       decimal_places=2,
                                       default=0.00)

    total = models.IntegerField(verbose_name="cost_order",
                                blank=False,
                                null=False,
    )
    shipping_address = models.CharField(max_length=150,
                                        blank=False,
                                        null=False)
    currency = models.CharField(max_length=5,
                                default="NPR")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"order by {self.user.username} in {self.created_at}"


class Order_items(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="order_items")
    name = models.CharField(verbose_name="name",
                            max_length=150)
    unit_price = models.DecimalField(verbose_name="price",
                                default=0.00,
                                decimal_places=2,
                                max_digits=12
                                )
    quantity = models.IntegerField(verbose_name="quantity",
                                   blank=False,
                                   null=False,
                                   default=1)
    subtotal = models.IntegerField(verbose_name="item total",
                                   blank=False,
                                   null=False,
                                   
                                   )
    product = models.ForeignKey(Products,
                                on_delete=models.SET_NULL,
                                related_name="in_order"
                                )

    def __str__(self):
        return f"{self.name} - {self.quantity} quantity "
    
  