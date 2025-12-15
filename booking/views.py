from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.models import Event, Ticket
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    exist_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()

    if exist_ticket:
        ticket = exist_ticket
        messages.info(request, "You already have a ticket for this event!")
    else:
        ticket = Ticket.objects.create(event=event, attendee=request.user)
        messages.success(request, "Ticket booked successfully!")

    return render(request, 'booking/ticket.html', {'ticket': ticket})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(attendee=request.user).select_related('event')
    return render(request, 'booking/my_tickets.html', {'tickets': tickets})


@require_http_methods(["POST"])
@login_required
def verify_ticket(request):
    data = json.loads(request.body)
    ticket_id = data.get('ticket_id')

    print('\nJson data: ' + data)

    try:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        return JsonResponse({
            'valid':True,
            'ticket_id': str(ticket.ticket_id),
            'event':ticket.event.title,
            'attendee': ticket.attendee.get_full_name() or ticket.attendee.username,
        })
    except Ticket.DoesNotExist:
        return JsonResponse({'valid':False, 'error': 'Ticket not found!!!'})
    

@login_required
def ticket_existed(request,event_id):
    pass
