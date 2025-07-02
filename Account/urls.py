from django.urls import path, include

from Account.views import  LoginView, RegisterView, OPLeaderView,SalesExecutiveView, AccountsManagerView, AdminView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('op-leader/', OPLeaderView.as_view(), name='op-leader-view'),
    path('se/',SalesExecutiveView.as_view(), name='sales-executive-view'),
    path('am/', AccountsManagerView.as_view(), name='account-manager-view'),
    path('admin/',AdminView.as_view(), name='admin-view'),
    
    ]