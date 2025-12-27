from django.urls import path 
from . import views 

app_name = 'organizers'

urlpatterns = [
    path('create-event/', views.create_event, name='create-event'),
    path('event-creator-registration/', views.event_creator_page, name='event-creator-page'),
    path('register-as-a-creator/', views.become_a_creator, name='register-creator'),
    path('success-page/', views.success_page, name="success-page"),
    path('event-creator-dashboard/', views.creator_dashboard, name='creator-dashboard'),
    path('view-event/<str:slug>/', views.view_event, name='view-event'),
    path('delete-event/<int:event_id>/', views.delete_event, name="delete-event"),
    path('edit-event/<int:event_id>/', views.edit_event, name="edit-event"),
    path('check-in-attendee/', views.check_in_attendee, name='check-in'),
    path('check-in-list/<int:event_id>/', views.checked_in_list, name='checked-in'),
    

    
]
