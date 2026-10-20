from apps.user.models import User
from django.db import models
from django.utils.text import slugify 
import uuid 
# Create your models here.


# with category as a diff model mean we have  a dynamic category and help in search too
class Category(models.Model):
    name = models.CharField(max_length=100,
                             unique=True)
    slug = models.SlugField(unique=True)


# product with id uuid prmary key and readable sku 
# discount need to be added with different system like coupon in consideration 
class Products(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    ) 
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            verbose_name="products_name ")
    sku = models.CharField(max_length=20,
                           blank=False,
                           null=False,
                           verbose_name="product_identifier",
                           unique=True)
    description = models.TextField(verbose_name="description")
    price = models.DecimalField(default=0.0,
                                null=False,
                                max_digits=10,
                                decimal_places=2,
                                  blank=False,
                                  verbose_name="price")
    stock = models.IntegerField(default=0,
                                verbose_name="product_stock")
    preserve = models.IntegerField(default=0,verbose_name='preserve')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        null=True
    )
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="products")
    active = models.BooleanField(verbose_name="active",
                                 default=False,
                                 null=False,
                                blank=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    def save(self,*args,**kwargs):
        if not self.sku:
            prefix = slugify(self.name).replace("-", "")[:3].upper()
            self.sku = f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
            
        super().save(*args,**kwargs)


    def __str__(self):
        return self.name
    

    
    