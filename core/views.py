from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Event, EventCategory, Ticket,LikedEvent,Organizer
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
import time
# Create your views here.

def index(request):
    events = Event.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('-created_at')[:8]
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


def browse_events(request):
    events = Event.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('-created_at')
    
    

    context = {
        'events':events,
        # 'events_query':events_query
    }

    return render(request, 'core/browse_events.html', context)
    

def browse_event_search(request):
    time.sleep(0.5)
    query = request.GET.get('search', '').strip()
    today = timezone.now().date()
    if query:

        events = Event.objects.filter(
            (
            Q(title__icontains=query) | 
            Q(location__icontains=query) |
            Q(event_tag__icontains=query)

            ) & Q(date__gte=today)
            
        )
    else:
        events = Event.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('-created_at')
        
    context = {
        'events':events,
    }

    return render(request, 'core/partials/browse_event_list.html', context)
    


#events details
def event_details(request,pk):
    event = get_object_or_404(Event, pk=pk)
    # exist_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    # if exist_ticket:
    #     return render(request, 'booking/event_booked_already.html', {"exist_ticket":exist_ticket})
    #organizer = get_object_or_404(Organizer, user=event.user)
    organizer = event.organizer
    context = {'event':event, 'organizer':organizer}
    return render(request, 'core/events_details.html',context)
    

# like event
def event_like(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, pk=event_id)
        #liked_events = LikedEvent.objects.all()
        if event.likes.filter(pk=request.user.id):
            event.likes.remove(request.user)
        else:
            event.likes.add(request.user)
        return render(request, 'core/partials/like_events.html', {'event':event})
        #return HttpResponse(event.likes.count())
        
    else:
        messages.info(request, "you are not logged in".title())
        return redirect('/')
   

#search for events
def search_event(request):
    time.sleep(1)
    query = request.GET.get('search', '').strip()
    today = timezone.now().date()
    if query:

        events = Event.objects.filter(
            (
            Q(title__icontains=query) | 
            Q(location__icontains=query) |
            Q(event_tag__icontains=query)

            ) & Q(date__gte=today)
          
        )
    else:
        events = Event.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('-created_at')
        
    context = {
        'events':events,
    }

    return render(request, 'core/partials/events_section.html', context)
    


def list_of_events_by_category(request, slug):
    time.sleep(1)
    event_category = get_object_or_404(EventCategory, slug=slug)
    current_date = timezone.now().date()
    events = Event.objects.filter(
        category=event_category,
         date__gte=current_date,
        )
    context = {
        'event_category':event_category,
        'events':events
    }
    return render(request,'core/partials/event_category_list.html',context)
    
