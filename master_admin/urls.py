from django.urls import path 
from . import views 

app_name = "master_admin"
urlpatterns = [
    path('',views.admin_dashboard, name='admin-dashboard' ),
    path('user-management/', views.user_management, name='user-management'),
]

