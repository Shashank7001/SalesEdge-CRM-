from django.urls import path

from Account.views import OPLeaderView
urlpatterns = [
   
    path('op-leader/', OPLeaderView.as_view(), name='op-leader-view'),
  
    ]
