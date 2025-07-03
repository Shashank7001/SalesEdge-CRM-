from django.urls import path

from Account.views import AccountsManagerView

urlpatterns = [
    path('am/', AccountsManagerView.as_view(), name='account-manager-view'), 
    ]
