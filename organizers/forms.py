from django import forms 
from core.models import Event 
from core.models import Organizer
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event 
        fields = ('category', 'event_tag', 'title', 'description', 'location', 'date', 'banner','price', 'total_tickets')
        exclude = ('available_tickets', 'user','oranizer')

    
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:border-blue-500 focus:ring-blue-500'
            })


       

        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg  focus:ring-2 focus:border-blue-500 focus:ring-blue-500 h-32'
        })

        self.fields['date'].widget.attrs.update({
            'class': 'datepicker w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:border-blue-500  '
        })

        self.fields['banner'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:border-blue-500 file:ml-1 file:py-2  file:rounded-md '
        })



class CreatorRegisterForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = "__all__"
        exclude = ["user", "creator"]

    momo_numb = PhoneNumberField(
        widget=RegionalPhoneNumberWidget(region='GH', attrs={
            'class':'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none',
            'placeholder': 'e.g +233244123456',
        })
    )
    
    
    def __init__(self, *args, **Kwargs):
        super().__init__(*args, **Kwargs)

        # for field in self.fields.values():
        #     field.widget.attrs.update({
        #         'class': 'w-full rounded-md border border-gray-300 px-4 py-2',
        #     })

        
        # self.fields['momo_numb'].widget.attrs.update({
        #     'class':'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none',
        #     'placeholder': 'e.g 0244 123 456',
            
        # })

        self.fields['email'].widget.attrs.update({
            'class':'w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none',
            'placeholder':'e.g example@gmail.com',
            
        })

        self.fields['full_name'].widget.attrs.update({
            'class':'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none',
            'placeholder':'e.g John Doe'

        })


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     for field in self.feilds.values():
    #         field.widget.attr.update({
    #             'class': 'w-full rounded-md px-4 py-2 border border-gray-300'
    #         })
