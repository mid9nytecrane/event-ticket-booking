from django.shortcuts import render,get_list_or_404
from core.models import Event, EventCategory, Organizer
from django.contrib.auth.models import User,Group 
from django.core.paginator import Paginator
from decimal import Decimal
# Create your views here.


def admin_dashboard(request):
    events = Event.objects.all()
    users = User.objects.all()
    
    #total number of users 
    users_count = users.count()
    #total number of events hosted on the platform
    events_count = events.count()
    #total events both upcoming and active (available events)
    available_events = sum(1 for event in events if event.is_active or event.is_upcoming)
    # pasted events
    past_events = sum(1 for event in events if event.is_past)

    # revenue for all non paid events
    total_revenue = sum(event.revenue for event in events if not event.is_paid)

    platform_revenue = (1 * total_revenue) / Decimal (0.95) 
    for_the_pocket = Decimal(platform_revenue - total_revenue)
    #print(f"y = {for_the_pocket}")

    context = {
        'users':users,
        'users_count':users_count,
        'events_count':events_count,
        'total_revenue':total_revenue,
        'available_events':available_events,
        'past_events':past_events,
        'for_the_pocket': for_the_pocket
    }

    return render(request, 'master_admin/dashboard.html', context)


def user_management(request):
    organizers = Organizer.objects.filter(user__groups__name="organizers")
    users = User.objects.all().exclude(pk=1) 
    attendees = []
   
    paginator = Paginator(organizers, 3)
    page_number = request.GET.get("page")
    organizers_list = paginator.get_page(page_number)
    
    #total users
    users_count = users.count()
    
    #organizers count
    organizers_count = organizers.count()

    users_with_group = users.prefetch_related('groups')
    for user in users_with_group:
        #print(f"user: {user}")
        if not user.groups.filter(name='organizers').exists():
            attendees.append(user)

    #attendees count
    attendees_count = len(attendees)

    print('list after ', attendees)

    #pagination for attendees
    paginator = Paginator(attendees, 3)
    page_number = request.GET.get('page')
    attendees_list = paginator.get_page(page_number)

   

    context = {
        'organizers_list':organizers_list,
        'users':users,
        'attendees_list': attendees_list,
        'users_count':users_count,
        'attendees_count':attendees_count,
        'organizers_count':organizers_count,
        
    }
    # if "HX-Request" in request.headers:
    #     return render(request, 'master_admin/partials/attendees_attendees_table_body.html',context)
    return render(request, 'master_admin/user_mng.html', context)