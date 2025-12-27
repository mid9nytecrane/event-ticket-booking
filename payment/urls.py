from django.urls import path 
from payment import views 

app_name = "payment"

urlpatterns = [
    path("initiate-payment/<int:event_id>/", views.user_validation, name='verify-user'),
    # path("make-payment", views.make_payment, name="make-payment"),
    path('verify-payment/<str:reference>/', views.verify_payment, name='verify-payment'),

    path('user-validation/<int:event_id>/', views.free_event_user_validation, name='validate-user'),
    

]
