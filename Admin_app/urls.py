from django.urls import path, include

from Admin_app.views import AdminView

urlpatterns = [    
    path('admin/',AdminView.as_view(), name='admin-view'),  
    ]
