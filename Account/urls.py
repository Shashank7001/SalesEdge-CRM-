from django.urls import path

from Account.views import  LoginView, RegisterView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    ]
