from rest_framework.permissions import (IsAdminUser,
                                        IsAuthenticated)
from rest_framework.generics import (CreateAPIView ,
                                     ListAPIView ,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     GenericAPIView,
                                     UpdateAPIView
                                     )
from django.contrib.auth import authenticate
from .serializers import ( Register_serializer ,    
                          Users_serializer ,
                          User_profile_serializer ,
                          LoginSerializer ,
                          Password_change_Serializer )
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
# Create your views here.

class user_create_view(CreateAPIView):
    serializer_class = Register_serializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
       
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

class Users_List(ListAPIView):
    serializer_class = Users_serializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

class Profile_View(RetrieveAPIView):
    serializer_class = User_profile_serializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return User.objects.filter(id =self.request.user.id)

class Login_View(GenericAPIView):
    serializer_class = LoginSerializer


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request,email=email,password=password)
        if user is None:
            return Response (
                {"detail": "invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)

        return Response(
                    {
                        "user": {
                            "id": user.id,
                            "email": user.email,
                        },
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

class Change_password(GenericAPIView):

    serializer_class = Password_change_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({
            "message":"password change sucessfully"
        },
            status=status.HTTP_200_OK
        )

class Logout_View(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        refresh_token = request.user.data.get('refresh')
        if not refresh_token:
            return Response({
                "error" : " provide refresh token "
            },
            status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken(refresh_token)
        refresh.blacklist()
        return Response({
            "message":"logout sucessfully "
        },
        status=status.HTTP_205_RESET_CONTENT
        )