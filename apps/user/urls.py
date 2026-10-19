from django.urls import path , include
from .views import ( Users_List,
                    user_create_view ,
                    Login_View,
                    Users_List,
                    Profile_View,
                    Change_password,
                    Logout_View
                    )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('registration/',user_create_view.as_view()),
    path('login/',Login_View.as_view()),
    path('users/',Users_List.as_view()),
    path('Profile/',Profile_View.as_view()),
    path('login/',user_create_view.as_view()),
    path('change_password',Change_password.as_view()),
    path('Logout/',Logout_View.as_view()),
    path('refresh/',TokenRefreshView.as_view()),

]