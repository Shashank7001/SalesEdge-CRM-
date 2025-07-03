from django.urls import path

from Account.views import  SalesExecutiveView

urlpatterns = [
    path('se/',SalesExecutiveView.as_view(), name='sales-executive-view'),
    ]
