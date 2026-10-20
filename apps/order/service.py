from decimal import Decimal
from django.db.models import F

from django.db import transaction
from yaml import serialize
from apps.cart.models import Cart_item , Cart
from apps.products.models import Products
from .models import Order_items , Order, Payment 
from rest_framework.exceptions import ValidationError
from apps.cart.serializers import Cart_view_serializer

 
@transaction.atomic
def checkout(*,user,data):

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        raise ValidationError("cart not initialize")
    
    cart_serializer = Cart_view_serializer(cart)
    cart_data = cart_serializer.data
    cart_items_data = cart_data.get("cart_item", [])
    if not cart_items_data:
        raise ValidationError("no cart item")
    orders_list = []
    total = Decimal("0.00")
    

    for item_data in cart_items_data:
        product_id = item_data['products']['id']
        quantity = item_data['quantity']

        if quantity <=  0:
            raise ValidationError("quantity cannot be negative and zero")
        try:
            product = Products.objects.get(id=product_id)
        except product.DoesNotExist:
            raise ValidationError("a product in cart doesnot exist")
        if not product.active:
            raise ValidationError("product is not  active")
        if product.stock < quantity:
            raise ValidationError({"stocks" :(f"{product.name} donot have sufficient in stocks avaiable")})
        unit_price = product.price
        subtotal = ((product.price  * ( 1 - product.discount/100) ) * quantity)
        total += subtotal
        orders_list.append({
            "product" : product,    
            "name" : product.name,
            "unit_price" : unit_price,
            "quantity" :   quantity,
            "subtotal" : subtotal
        })

    shipping_fee = 0
    total += shipping_fee


    for order_item in orders_list:
        updated = Products.objects.filter(
            pk=order_item["product"].pk,
            active=True,
            stock__gte=order_item["quantity"],
        ).update(
            stock=(
                F("stock") - order_item["quantity"]
            )
        )

        if updated != 1:
            raise ValidationError({
                "stock": (
                    f"Stock changed for {order_item['name']}. "
                    "Please try checkout again."
                )
            })

    order = Order.objects.create(
        user=user,
        shipping_address=data["shipping_address"],
        shipping_fee=shipping_fee,
        total=total,
        currency="NPR",
        status="pending",
    )

    Order_items.objects.bulk_create([
        Order_items(
            
            order=order,
            product=items["product"],
            name=items["name"],
            quantity=items["quantity"],
            unit_price=items["unit_price"],
            subtotal=items["subtotal"],
        )
        for items in orders_list
    ])

    
    Cart_item.objects.filter(cart=cart).delete()

    return order

@transaction.atomic
def Cancelled(*,user,orderid):
    try:
        order_obj = Order.objects.get(id=orderid,user=user)
    except Order.DoesNotExist:
        raise ValidationError("order doesnot exists")
    print(order_obj.status)
    if order_obj.status not in ['pending','confirmed']:
        raise ValidationError("can only cancelled  before shipment")
    order_items = list(Order_items.objects.filter(order=order_obj))


    for item in order_items:
        Products.objects.filter(pk=item.product.pk).update(stock=F("stock")+item.quantity)

    order_obj.status = "cancelled"

    order_obj.save(update_fields=['status','updated_at'])

    return order_obj
