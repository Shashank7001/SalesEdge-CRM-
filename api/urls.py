
from django.urls import path, include

urlpatterns = [
    path('account/', include('Account.urls')),
    path('admin/', include('Admin_app.urls')),
    path('op/', include('OP_app.urls')),
    path('acc/', include('Acc_app.urls')),
    path('sales/', include('SalesEx.urls')),
   
]