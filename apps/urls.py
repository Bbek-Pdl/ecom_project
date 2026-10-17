from django.urls import path , include

urlpatterns = [
    path('cart/',include('cart.urls')),
    path('products/',include('products.urls')),
    path('user/',include('user.urls')),
    path('order/',include('order.urls'))
]