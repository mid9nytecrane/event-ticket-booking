from django.shortcuts import render
from django.contrib import messages
from allauth.account.views import SignupView, LoginView  
from allauth.account import app_settings 


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
                f"Welcome {form.cleaned_data['first_name']} . Your account has been created."
            )
        
        return response


class Custom_LoginView(LoginView):
    pass 



