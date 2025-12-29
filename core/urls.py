from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static
from user_account.views import user_profile,update_profile

from . import views 

urlpatterns = [
    path('',views.index, name='index-page'),
    path('browse-events/', views.browse_events, name='browse-event'),
    path('event_details/<int:pk>/', views.event_details, name='event-detail'),
    path('search_event/',views.search_event, name='search-event'),
    path('event_category/<slug:slug>/',views.list_of_events_by_category, name='category-events'),
    path('event_like/<int:event_id>/', views.event_like, name="event-like"),

    path('profile-page/', user_profile, name='user-profile'),
    path('profile-update/', update_profile, name='update-profile'),
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
