from django.shortcuts import render,get_object_or_404
from .models import Event, EventCategory
from django.core.paginator import Paginator
from django.db.models import Q

import time
# Create your views here.

def index(request):
    events = Event.objects.all().order_by('-created_at')
    event_categories = EventCategory.objects.all()

    paginator = Paginator(events, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    

    context = {
        'events':events,
        'event_categories': event_categories,
        'page_obj':page_obj,
    }
    return render(request, 'core/index.html', context)


#events details
def event_details(request,pk):
    event = get_object_or_404(Event, pk=pk)
    context = {'event':event}
    return render(request, 'core/events_details.html',context)
    


#search for events
def search_event(request):
    time.sleep(1)
    query = request.GET.get('search', '').strip()
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | 
            Q(location__icontains=query) |
            Q(event_tag__icontains=query)
        )
    else:
        events = Event.objects.all()
        
    context = {
        'events':events,
    }

    return render(request, 'core/partials/events_section.html', context)
    


def list_of_events_by_category(request, slug):
    time.sleep(1)
    event_category = get_object_or_404(EventCategory, slug=slug)
    events = Event.objects.filter(category=event_category)
    context = {
        'event_category':event_category,
        'events':events
    }
    return render(request,'core/partials/event_category_list.html',context)
    
