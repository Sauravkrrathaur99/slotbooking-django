# from django import forms
# from .models import InterviewSlot

# class SlotBookingForm(forms.Form):
#     selected_slot = forms.ModelChoiceField(
#         queryset=InterviewSlot.objects.filter(is_booked=False),
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Select a slot",
#     )


# class SlotBookingForm(forms.Form):
#     selected_slot = forms.ModelChoiceField(
#         queryset=InterviewSlot.objects.none(),
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Select a slot",
#         to_field_name="id",  # Specify that the 'id' should be used as the value
#     )


# forms.py
from django import forms
from .models import InterviewSlot

# class SlotBookingForm(forms.ModelForm):
#     class Meta:
#         model = InterviewSlot
#         fields = []

#     slot = forms.ModelChoiceField(
#         queryset=InterviewSlot.objects.filter(is_booked=False),
#         empty_label="Available Slots For You",
#         label="Select Your Slots: ",
#         widget=forms.Select(attrs={'class': 'form-control'}),  
#     )


# class SlotBookingForm(forms.ModelForm):
#     class Meta:
#         model = InterviewSlot
#         fields = ['email', 'slot']


#     email = forms.EmailField(
#             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}),
#     )

#     slot = forms.ModelChoiceField(
#         queryset=InterviewSlot.objects.filter(is_booked=False),
        
#         widget=forms.Select(attrs={'class': 'form-control'}),
#     )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Add Bootstrap CSS classes to form elements
    #     self.fields['slot'].widget.attrs['class'] = 'form-control'
    #     self.fields['slot'].label = ''
    #     self.fields['email'].label = ''
    #     self.fields['slot'].empty_label = None


class SlotBookingForm(forms.ModelForm):
    class Meta:
        model = InterviewSlot
        fields = []

    slot = forms.ModelChoiceField(
        queryset=InterviewSlot.objects.filter(is_booked=False),
        empty_label="Available Slots For You",
        
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap CSS classes to form elements
        self.fields['slot'].widget.attrs['class'] = 'form-control'
        self.fields['slot'].label = ''
        self.fields['email'].label = ''
        self.fields['slot'].empty_label = None