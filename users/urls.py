
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as authentication_views
# name space : url NAME
app_name="users"

urlpatterns = [
      path("register/",views.register,name="register"),
      path("login/",authentication_views.LoginView.as_view(template_name='temp/login.html'),name="login"),
      path("logout/",authentication_views.LogoutView.as_view(template_name='temp/logout.html',),name="logout"),
      path('profile/',views.profile,name="profile"),
      path('createprofile/',views.create_profile,name="create_profile"),
      path('sellerprofile/<int:id>/',views.seller_profile,name="seller_profile")
]    
    
