from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from . models import UserProfile
from .forms import CustomSignUpForm
from django.dispatch import  receiver


@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        form_data =CustomSignUpForm
        UserProfile.objects.create(
            user=instance,
          
            
        )

        print(f"\n{instance.username}'s profile is created.")
    else:
        print("\nUser profile not created !!")