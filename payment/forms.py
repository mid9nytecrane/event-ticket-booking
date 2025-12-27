from django import forms 

from .models import FreeEventRegisterInfo, Payment


class FreeEventRegisterForm(forms.ModelForm):

    class Meta:
        model = FreeEventRegisterInfo
        fields = ('email', 'full_name','contact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'w-full px-3 py-2 rounded-md'
            })



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




