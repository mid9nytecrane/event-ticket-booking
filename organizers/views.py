from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,permission_required
from .forms import CreateEventForm, CreatorRegisterForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from core.models import Event,Ticket,Organizer
import datetime
# Create your views here.

@login_required
#@permission_required('core.add_event')
#@require_http_methods(["POST"])
def create_event(request):
    if request.user.has_perm('core.add_event'):
        form = CreateEventForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.user = request.user 
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
            HttpResponse('form is invalid')

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
        events = Event.objects.filter(user=request.user)
        tickets = Ticket.objects.filter(is_used=True)

        # for event in events:
        #     print(f"{event} id: {event.id}")
            
        #     revenue = event.price * event.purchased_tickets
        total_revenue = sum(event.revenue for event in events)
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
            
        }
        return render(request, "organizers/dashboard.html", context)
    else:
        return HttpResponse("you are not authorized to view this page.")



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
        return render(request, 'organizers/edit_event.html', {'form':form})


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


