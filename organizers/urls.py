from django.urls import path 
from . import views 

app_name = 'organizers'

urlpatterns = [
    path('create-event/', views.create_event, name='create-event'),
    path('register-as-a-creator/', views.become_a_creator, name='register-creator'),
    path('event-creator-dashboard/', views.creator_dashboard, name='creator-dashboard'),

    
]
