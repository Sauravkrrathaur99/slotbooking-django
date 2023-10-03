
# forms.py
from django import forms
from .models import InterviewSlot

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

        # Format the choices for the slot field
        self.fields['slot'].choices = self.get_formatted_slot_choices()

    def get_formatted_slot_choices(self):
        # Order the slots by date and time in ascending order
        slots = InterviewSlot.objects.filter(is_booked=False).order_by('date', 'time_start')
        # Create a list of formatted choices
        formatted_choices = []
        for slot in slots:
            formatted_date = slot.date.strftime('%d-%m-%Y')
            formatted_time = f"{slot.time_start.strftime('%I:%M %p')} - {slot.time_end.strftime('%I:%M %p')}"
            formatted_choices.append((slot.id, f"{formatted_date} [{formatted_time}]"))
        return formatted_choices