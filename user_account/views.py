from django.shortcuts import render, HttpResponse,get_object_or_404
from django.contrib import messages
from allauth.account.views import SignupView, LoginView  
from allauth.account import app_settings 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import UserProfile
from .forms import ProfileUpdateForm


class CustomSignupView(SignupView):
    def form_valid(self, form):

        response = super().form_valid(form)

        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            messages.info(
                self.request,
                "We've sent you an email for verification, please check your inbox"
            )
        else:
            messages.success(
                self.request,
                f"Welcome {self.request.user.username} . Your account has been created."
            )
        
        return response


class Custom_LoginView(LoginView):
    pass 


# user profile page
@login_required
def user_profile(request):
    userprofile = UserProfile.objects.filter(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    context  = {
        'userprofile':userprofile,
        'form': ProfileUpdateForm(instance=profile)
    }
    return render(request, 'core/auth/user_profile.html', context)


@login_required
#@require_http_methods(["POST"])
def update_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    userprofile = UserProfile.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()

            context = {'form':form, 
                       'profile':profile,
                       'userprofile':userprofile,
                       
                       }
            return render(request, 'core/auth/partials/personal_info.html', context)
           
        else:
            HttpResponse("data enter is invalid!!!")
        #return render(request, 'core/auth/partials/update_profile_modal.html', {'form':form})
    
        context = {
            
            'profile': profile,
            'form': form,
            'userprofile':userprofile,
        }
    else:
        form = ProfileUpdateForm(instance=profile)
        return render(request, 'core/auth/partials/update_profile_modal.html',context)
    # response['HX-TRIGGER'] = "update-success"
    # return response
    




