from django.db import models
from django.contrib.auth.models import User 
from payment.paystack import Paystack
from core.models import Event
import uuid
# Create your models here.


class FreeEventRegisterInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='free_event_info')
    email = models.EmailField()
    contact = models.CharField(max_length=12 , null=True)
    full_name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.full_name}({self.user}) ticket for {self.event}"
        

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True, related_name="event")
    amount = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    reference = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.amount} for {self.event.title}"
    
    def amount_value(self):
        return int(float(self.amount)* 100)
    
   

    def verify_payment(self):
        paystack = Paystack()
        # print(f"\nreference from model.py: {self.reference}")
        # print(f"amount: {self.amount}")

        status, result = paystack.verify_payment(self.reference, self.amount)

        # print(f"\nstatus: {status}")
        # print(f"result: {result}")

        if status:
            
            print(type(result['amount']))
            print(type(self.amount))
         
            if float((result['amount'] / 100)) == float(self.amount):
                self.verified = True 
                self.save()

        if self.verified:
            return True 
        else:
            return False 
        
        
        



