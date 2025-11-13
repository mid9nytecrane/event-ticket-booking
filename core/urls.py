from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('',views.index, name='index-page'),
    path('event_details/<int:pk>/', views.event_details, name='event-detail'),
    path('search_event/',views.search_event, name='search-event'),
    path('event_category/<slug:slug>/',views.list_of_events_by_category, name='category-events'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
