from django.contrib.auth.models import User
from core.models import Ticket
from user_account.models import UserProfile
from user_account.forms import CustomSignUpForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File 

import qrcode 
from io import BytesIO


#creating user profile
@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile(sender,created,instance, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            email=instance.email,
        )

        print(f"\n{instance.username}'s profile is created.")
    else:
        print("\nUser profile not created !!")    


@receiver(post_save,sender=Ticket, dispatch_uid='generate_qr_code')
def generate_qr_code(sender, instance, created, **kwargs):
    print('\nsignal fired !!!')
    if created or not instance.qr_code:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        #qr code data
        qr_data = f"""
               TicketId: {instance.ticket_id}
                Event: {instance.event.title}
                Attendee: {instance.attendee.username}
            """
        
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)

        filename = f"qr_code_{instance.ticket_id}.png"
    
        instance.qr_code.save(filename, File(buffer),   save=False)
        instance.save()

        print(f"✅ QRCode save for {instance.ticket_id}")