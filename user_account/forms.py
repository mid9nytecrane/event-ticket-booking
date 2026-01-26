from django import forms 
from .models import UserProfile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget,RegionalPhoneNumberWidget

class CustomSignUpForm(forms.Form):
    # first_name = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    # )
    # last_name = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    # )

    phone = PhoneNumberField(
        widget=RegionalPhoneNumberWidget(region='GH', attrs={
            'placeholder': 'e.g +23324xxxxxx'
        })
    )

    # town = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'placeholder': 'City/Town'})
    # )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'example@gmail.com'
    }))
    


    def signup(self,request,user):
        """called after user is created but before saved to handle additional 
            fields
        """
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        # user.phone = self.cleaned_data.get('town', '')
        user.save()


#profile update 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude=["user"]


    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'rounded-lg py-2 px-3 w-full'
            })
            