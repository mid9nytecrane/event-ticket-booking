from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,permission_required
from .forms import CreateEventForm, CreatorRegisterForm
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator
from django.contrib import messages
from core.models import Event,Ticket,Organizer
from django.db.models import Q
import datetime
from django.utils import timezone
# Create your views here.

@login_required
#@permission_required('core.add_event')
#@require_http_methods(["POST"])
def create_event(request):
    
    if request.user.has_perm('core.add_event'):
        organizer = Organizer.objects.get(user=request.user)
        form = CreateEventForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.user = request.user
                form_instance.organizer = organizer
                form_instance.save()

                return redirect('organizers:creator-dashboard')
            else:
                return HttpResponse("data inputed is invalid!!!")
        else:
            form = CreateEventForm()
            print(form.errors)
            return render(request,'organizers/create_event.html', {'form':form})

    else:
        return HttpResponse("You not authorised to visit this page")



def event_creator_page(request):
    
    return render(request, "organizers/creator_page.html", )


@login_required
def become_a_creator(request):
    form = CreatorRegisterForm(request.POST)
    # try:
    #     event_creator = get_object_or_404(Organizer, user=request.user)
    #     return redirect("organizers:creator-dashboard")
    # except Organizer.DoesNotExist:
       # event_creator = None
    if request.method == "POST":
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user 
            form_instance.creator = True
            form.instance.save()

            # assigning user to a creator/organizers group
            user = request.user
            organizers_group, created = Group.objects.get_or_create(name="organizers")
            user.groups.add(organizers_group)

            return redirect("organizers:success-page")
        else:
            messages.error(request, "form contains invalid data, check and enter valid data inputs")

    else:
        form = CreatorRegisterForm()
    context = {
        'form':form,
        #'event_creator':event_creator
        }

    return render(request, 'organizers/creator_register.html', context)


@login_required
def success_page(request):

    context = {}
    return render(request, 'organizers/partials/success_page.html', context)



@login_required
def creator_dashboard(request):
    if request.user.groups.filter(name="organizers"):
        events = Event.objects.filter(user=request.user).order_by('-created_at')
        tickets = Ticket.objects.filter(is_used=True)
        current_date = timezone.now()
        #filter events
        query = request.GET.get('filter', '')
        if query:
            query_events = events.filter(
                Q(title__icontains=query) | 
                Q(status__icontains=query) |
                Q(payment_status__icontains=query)
                
            )
        else:
            query_events = events
            
        #pagination
        paginator = Paginator(query_events, 3)
        page_number = request.GET.get("page")
        events_list = paginator.get_page(page_number)

        nums = "a" * paginator.num_pages
        # for event in events:
        #     print(f"{event} id: {event.id}")
            
        #     revenue = event.price * event.purchased_tickets
        for event in events:
            if event.is_upcoming:
                Event.objects.filter(pk=event.id).update(status="upcoming")
            elif event.is_active:
                Event.objects.filter(pk=event.id).update(status='active')
            else:
                Event.objects.filter(pk=event.id).update(status='past')
        
        for event in events:
            if event.is_paid:
                Event.objects.filter(pk=event.id).update(payment_status='paid')
            else:
                Event.objects.filter(pk=event.id).update(payment_status='pending')
            
            
        total_revenue = sum(event.revenue for event in events if not event.is_paid)
        total_tickets_sold = sum(event.total_purchased_tickets for event in events)

        active_events_count = sum(1 for event in events if event.is_active)
        active_event_list = [event for event in events if event.is_active]

        upcoming_events_count = sum(1 for event in events if event.is_upcoming)
        upcoming_events_list = [event for event in events if event.is_upcoming]

        

        print(f"\nActive Events: {active_events_count}")
        print(f"active event: {active_event_list}")

        print(f"\nupcoming events count: {upcoming_events_count}")
        print(f"upcoming events: {upcoming_events_list}")

        context = {
            'events':events,
            'total_revenue':total_revenue,
            'total_tickets_sold':total_tickets_sold,
            'active_events_count':active_events_count,
            'upcoming_events_count':upcoming_events_count,          
            'tickets':tickets,
            'current_date':current_date,
            'events_list': events_list,
            'active_event_list': active_event_list,
            'page_range':events_list.paginator.page_range,
            
        }
        if "HX-Request" in request.headers:
            return render(request, 'organizers/partials/event_table_body.html', context)
        return render(request, "organizers/dashboard.html", context)
    else:
        return HttpResponse("you are not authorized to view this page.")


#filter events
# def filter_events(request):
#     query = request.GET.get('filter', '')
#     if query:
#         events_list  = Event.objects.filter(
#             title__icontains=query
            
#         )
#     else:
#         events_list = Event.objects.all()

#     context = {
#         'events_list':events_list,
#     }
#     return render(request, 'organizers/partials/event_table_body.html', context)


@login_required
def view_event(request, slug):
    if request.user.has_perm('core.view_event'):
        event = get_object_or_404(Event, pk=slug)
        context = {'event':event}

        return render(request, 'organizers/view_event.html', context)
    else:
        return HttpResponse('You are not authorized to view this page')


@login_required
@require_http_methods(["POST"])
def delete_event(request, event_id):
    
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    event.delete()
    context = {'event':event}
    messages.success(request, f"{event.title} has been deleted")
    return redirect("organizers:creator-dashboard")
    



@login_required
#@require_http_methods(["POST"])
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    first_buy = event.total_purchased_tickets >= 1
    form = CreateEventForm(request.POST, request.FILES, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            messages.success(request, f"{event.title} is updated success")
            return redirect("organizers:creator-dashboard")
        
        else:
            messages.success(request, f" invalid data , {event.title} is not updated")

    else:
        form = CreateEventForm(instance=event)
        return render(request, 'organizers/edit_event.html', {
            'form':form,
            'event':event,
            'first_buy':first_buy,
            })


#checking-in attendees i.e this scanning and manually entery ticket data
@login_required
def check_in_attendee(request):
   
    return render(request, 'organizers/check_in_attendee.html')

@login_required
def checked_in_list(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)

    checked_in = Ticket.objects.filter(
        event=event,
        is_used = True,

    ).select_related("attendee")

    context = {
        'event': event,
        'checked_in':checked_in,
    }

    return render(request, 'organizers/check_in_list.html', context)



