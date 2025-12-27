from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from core.models import Event, Ticket
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    exist_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    success = event.register_free_tickets() #method from the core/models.py

    if exist_ticket:
        ticket = exist_ticket
        messages.info(request, "You already have a ticket for this event!")
    else:
        if success:
            ticket = Ticket.objects.create(event=event, attendee=request.user)
            messages.success(request, "Ticket booked successfully!")
        else:
            ticket = Ticket.objects.create(event=event, attendee=request.user)
            messages.success(request, "Ticket booked successfully!")
        

    return render(request, 'booking/ticket.html', {'ticket': ticket})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(attendee=request.user).select_related('event')
    return render(request, 'booking/my_tickets.html', {'tickets': tickets})



@require_http_methods(["GET","POST"])
@login_required
def verify_ticket(request):
    # data = json.loads(request.body)
    # ticket_id = data.get('ticket_id')
    ticket_id = None 
    
    # if request is JSON
    if request.headers.get("Content-Type") == "application/json":
        try:
            data = json.loads(request.body)
            ticket_id = data.get("ticket_id")
        except:
            pass 

    # if request is POST 
    elif request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
    
    else:
        ticket_id = request.GET.get('ticket_id')

    if not ticket_id:
        return HttpResponse("""
            <div class="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 mt-4 shadow-sm">
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                    </svg>
                    <span class="font-semibold">Check-in Failed</span>
                </div>
                <p class="mt-2 text-sm">No ticket ID provided. Please enter a ticket code.</p>
            </div>
        """)
    
    

    try:
        #ticket = Ticket.objects.select_related("event", "attendee").get(ticket_id=ticket_id)
        ticket = Ticket.objects.select_related('event').get(ticket_id=ticket_id)
        event = ticket.event 

        # ----- SECURITY CHECK-------
        if event.user != request.user:
            
             return HttpResponse("""
                <div class="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 mt-4 shadow-sm">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                        </svg>
                        <span class="font-semibold">Unauthorized</span>
                    </div>
                    <p class="mt-2 text-sm">This ticket does not belong to your event.</p>
                </div>
            """)
        

        # ------- Checking if Ticket matches Day of Event --------- 
        if not event.is_active:
            
           return HttpResponse(f"""
                <div class="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 mt-4 shadow-sm">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                        </svg>
                        <span class="font-semibold">Event Not Active</span>
                    </div>
                    <p class="mt-2 text-sm">This ticket is not valid for today's event.</p>
                    <p class="mt-1 text-xs opacity-80">Event date: {event.date.strftime('%B %d, %Y')}</p>
                </div>
            """)


        # ------- Already Checked In
        if ticket.is_used:
            
             return HttpResponse(f"""
                <div class="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-xl p-4 mt-4 shadow-sm">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                        </svg>
                        <span class="font-semibold">Already Checked In</span>
                    </div>
                    <p class="mt-2 text-sm">Ticket is already checked in or used.</p>
                    <div class="mt-2 p-2 bg-white/50 rounded-lg">
                        <p class="text-xs"><span class="font-medium">Event:</span> {ticket.event.title.title()}</p>
                        <p class="text-xs"><span class="font-medium">Attendee:</span> {ticket.attendee.get_full_name() or ticket.attendee.username}</p>
                    </div>
                </div>
            """)
        
        # ------- Mark As Used --------
        ticket.is_used = True 
        ticket.checked_in_at = timezone.now()
        ticket.save()


        # return JsonResponse({
        #     "valid":True,
        #     "status":"success",
        #     "message":"Check-in Successfully",
        #     "ticket_Id": ticket.ticket_id,
        #     "event": event.title,
        #     "attendee":ticket.attendee.get_full_name() or event.attendee.username,
        #     "time": timezone.now().strftime("%I:%M %p")
        # })

        return HttpResponse(f"""
            <div class="bg-green-50 border border-green-200 text-green-800 rounded-xl p-4 mt-4 shadow-sm">
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    <span class="font-semibold">Check-in Successful!</span>
                </div>
                <p class="mt-2 text-sm">Ticket <strong>{ticket.ticket_id}</strong> has been checked in successfully.</p>
                <div class="mt-3 p-3 bg-white/50 rounded-lg">
                    <p class="text-sm"><span class="font-medium">Event:</span> {ticket.event.title.title()}</p>
                    <p class="text-sm"><span class="font-medium">Attendee:</span> {ticket.attendee.get_full_name() or ticket.attendee.username}</p>
                    <p class="text-xs opacity-70 mt-1">Checked in at: {timezone.now().strftime('%I:%M %p')}</p>
                </div>
            </div>
        """)
    except Ticket.DoesNotExist:
        return JsonResponse({
            "valid":False,
            "status": "not found", 
            "message": "Ticket not found"
        }, status=500)
    

@login_required
def verify_ticket_by_scan(request):
    ticket_id = None 
    
    # if request is JSON
    if request.headers.get("Content-Type") == "application/json":
        try:
            data = json.loads(request.body)
            ticket_id = data.get("ticket_id")
        except:
            pass 

    # if request is POST 
    elif request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
    
    else:
        ticket_id = request.GET.get('ticket_id')

    try:
        ticket = Ticket.objects.select_related('event').get(ticket_id=ticket_id)

        event = ticket.event 

        if event.user != request.user:
            return JsonResponse({
                'valid':False,
                'status':'unathorized',
                'message': 'Ticket does not belong this event'
            })
        
        if not event.is_active:
            return JsonResponse({
                "valid":False,
                "status":"inactive",
                "message": "This is ticket is not valid for today's event",
                "details":{
                    "ticket date": event.date
                }
            })
        
        if ticket.is_used:
            return JsonResponse({
                "valid":False,
                "status":"already",
                "message": "Ticket is already used or checked in",
                "event":ticket.event.title,
                "attendee": ticket.attendee.get_full_name() or ticket.attendee.username
            })
        
        ticket.is_used = True 
        ticket.checked_in_at = timezone.now()
        ticket.save()

        return JsonResponse({
            "valid":True, 
            "status": "success",
            "message": "Check in Successful",
            "event": ticket.event.title,
            "attendee": ticket.attendee.get_full_name() or ticket.attendee.username,
        })
    
    except Ticket.DoesNotExist:
        return JsonResponse({
            "valid":False,
            "status": "not found", 
            "message": "Ticket not found"
        }, status=500)