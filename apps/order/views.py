from django.shortcuts import render
from .models import (Order,
                    Order_items,
                    Products)
from .serializers import (Order_Checkout_View)
from rest_framework.generics import (GenericAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     )

# Create your views here.

class Checkout_view(CreateAPIView):
    serializer_class = Order_Checkout_View

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()  #instance of order created
        

        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    

