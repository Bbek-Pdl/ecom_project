from django.urls import path , include

urlpatterns = [
    path('cart/',include('apps.cart.urls')),
    path('products/',include('apps.products.urls')),
    path('user/',include('apps.user.urls')),
    path('order/',include('apps.order.urls')),
]