from django import forms 

from .models import FreeEventRegisterInfo, Payment


class FreeEventRegisterForm(forms.ModelForm):

    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={
        'class': 'w-full p-4 rounded-md border border-gray-800 mb-4',

        'placeholder': 'example.com',
    }))


    full_name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={
        'class': 'w-full p-4 rounded-md border border-gray-800 mb-4',

        'placeholder': 'your full name',
    }))

    contact = forms.CharField(label="Contact", widget=forms.TextInput(attrs={
        'class': 'w-full p-4 rounded-md border border-gray-800 mb-4',

        'placeholder': '+233XXXXXXXXXXX',
    }))
    class Meta:
        model = FreeEventRegisterInfo
        fields = ('email', 'full_name','contact')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("email",)

    
    def __init__(self, *args, **Kwargs):
        super().__init__(*args, **Kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 rounded-md'
            })




