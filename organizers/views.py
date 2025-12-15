from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import CreateEventForm, CreatorRegisterForm
from django.contrib.auth.models import User, Group, Permission

from core.models import Event
# Create your views here.

@login_required
#require_http_methods(["POST"])
def create_event(request):
    form = CreateEventForm(request.POST, request.FILES)
    if request.method == "POST": 
        if form.is_valid():
            
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            
            form_instance.save()

            return redirect('/')
        else:
            HttpResponse('form is invalid')
            print(form.errors)

    else:
        form = CreateEventForm()
    context = {

        'form': form,
    }
    return render(request, 'organizers/create_event.html', context)


@login_required
def become_a_creator(request):
    form = CreatorRegisterForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user 
            form.instance.save()

            # assigning user to a creator/organizers group
            user = request.user
            organizers_group, created = Group.objects.get_or_create(name="organizers")
            user.groups.add(organizers_group)

            return redirect('/')
        else:
            HttpResponse('form is invalid')

    else:
        form = CreatorRegisterForm()
    context = {'form':form}

    return render(request, 'organizers/creator_register.html', context)



@login_required
def creator_dashboard(request):
    events = Event.objects.filter(user=request.user)

    for event in events:
        print(f"{event} id: {event.id}")

    context = {
        'events':events,
        #'revenue':revenue,
    }
    return render(request, "organizers/dashboard.html", context)
