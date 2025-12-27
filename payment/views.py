from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import FreeEventRegisterForm, PaymentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from core.models import Event, Ticket
from payment.models import Payment
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse

import uuid



@login_required
def user_validation(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    ref = f"booked_{uuid.uuid4().hex[:12].upper()}"
    paystack_pub_key = settings.PAYSTACK_PUBLIC_KEY

    exist_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    if exist_ticket:
        return render(request, 'booking/event_booked_already.html', {"exist_ticket":exist_ticket})
        
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            if event.purchased_tickets >= event.total_tickets:
                messages.error(request, "Sorry, ticket is sold out")
                return redirect('event-detail', pk=event.id)
            payment = form.save(commit=False)
            payment.user = request.user 
            payment.event = event
            payment.reference = ref
            payment.amount = event.price
            payment.save()

            return render(request, 'payment/make_payment.html', {
                'payment':payment,
                'paystack_pub_key':paystack_pub_key
            })
            
        
    else:
        form = PaymentForm()

    return render(request, 'payment/user_validation.html', {
        'form':form,
        
    })



@login_required
def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    event_id = payment.event.id
    verified = payment.verify_payment()

    event = get_object_or_404(Event, pk=event_id)
    total_tickets = event.total_tickets
    

    # getting current purchased tickets
    current_purchased_tickets = event.purchased_tickets
    current_total_tickets = event.total_tickets

    # print(f"\n{event} has {total_tickets} tickers in total")
    # print(f"current purchased tickets for {event} is: {current_purchased_tickets}")
    
    if verified:
        if current_purchased_tickets <= current_total_tickets:
            new_purchased_tickets = current_purchased_tickets + 1
            #new_total_tickets = current_total_tickets - 1

            Event.objects.filter(
                pk=event_id, purchased_tickets=current_purchased_tickets
                ).update(purchased_tickets=new_purchased_tickets)
            
            messages.success(request, "validation successful")

    else:
        messages.error(request, "validation failed")

    return redirect("booking:book-event", event_id=event_id)



# free booking or getting free tickets
@login_required
def free_event_user_validation(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    exist_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    if exist_ticket:
        return render(request, 'booking/event_booked_already.html', {"exist_ticket":exist_ticket})
    form = FreeEventRegisterForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            if event.purchased_tickets >= event.total_tickets:
                messages.error(request, "Sorry, tickets are sold out")
                return redirect("event-detail", pk=event.id)
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.event = event
            form_instance.save()
            return redirect("booking:book-event", event_id=event.id)
      
    else:   
        form = FreeEventRegisterForm()
        print("invalid data input")
    return render(request, 'payment/free_event_user_validation.html', {
        'form':form,
        'event':event,
    })













