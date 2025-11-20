from django import forms 


class CustomSignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    phone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'e.g 024XXXXXXX'})
    )

    town = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'City/Town'})
    )
    


    def signup(self,request,user):
        """called after user is created but before saved to handle additional 
            fields
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.phone = self.cleaned_data.get('phone', '')
        # user.phone = self.cleaned_data.get('town', '')
        user.save()
