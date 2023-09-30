# from django.shortcuts import render
# from .forms import SlotBookingForm

# # def slot_booking(request):
# #     if request.method == 'POST':
# #         form = SlotBookingForm(request.POST)
# #         if form.is_valid():
# #             # Add logic to check if the selected slot is available and save it if available
# #             # For example, you can check if the slot is already booked by another candidate
# #             # If it's available, you can mark it as booked and save it to the database
# #             # You can also associate the slot with the candidate, if needed.
# #             form.save()
# #             # Redirect to a success page or a thank you page
# #             return render(request, 'thank_you.html')
# #     else:
# #         form = SlotBookingForm()

# #     return render(request, 'slotbooking.html', {'form': form})


# from django.shortcuts import render, redirect
# from .models import InterviewSlot
# from .forms import SlotBookingForm

# def slot_booking(request):
#     available_slots = InterviewSlot.objects.filter(is_booked=False)
#     if request.method == 'POST':
#         form = SlotBookingForm(request.POST, available_slots=available_slots)
#         if form.is_valid():
#             selected_slot_id = form.cleaned_data['selected_slot']
#             selected_slot = InterviewSlot.objects.get(pk=selected_slot_id)
#             selected_slot.is_booked = True
#             selected_slot.save()
#             return redirect('thank_you')
#     else:
#         form = SlotBookingForm(available_slots=available_slots)
#     return render(request, 'slotbooking.html', {'form': form, 'available_slots': available_slots})



# from django.shortcuts import render, redirect
# from .models import InterviewSlot
# from .forms import SlotBookingForm

# def slot_booking(request):
#     # Filter available slots that are not booked
#     available_slots = InterviewSlot.objects.filter(is_booked=False)
    
#     if request.method == 'POST':
#         form = SlotBookingForm(request.POST)
#         form.fields['selected_slot'].queryset = available_slots  # Set the queryset
#         if form.is_valid():
#             selected_slot_id = form.cleaned_data['selected_slot']
#             selected_slot = InterviewSlot.objects.get(pk=selected_slot_id)
#             selected_slot.is_booked = True
#             selected_slot.save()
#             return redirect('thank_you')
#     else:
#         form = SlotBookingForm()
#         form.fields['selected_slot'].queryset = available_slots  # Set the queryset

#     return render(request, 'slotbooking.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from slotbooking_app.models import BookedSlots, InterviewSlot, MeetingLink
from .forms import SlotBookingForm
from django.core.mail import send_mail
import datetime
from django.core.mail import EmailMultiAlternatives

def slot_booking(request):
    time_slots = InterviewSlot.objects.all()
    current_year = datetime.datetime.now().year
    try:
        common_meeting_link = MeetingLink.objects.first().link
    except MeetingLink.DoesNotExist:
        common_meeting_link = None
    if request.method == "POST":
        form = SlotBookingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            selected_slot = form.cleaned_data["slot"]
            selected_slot.is_booked = True
            selected_slot.save()
            # Create and save a new instance of BookedSlots
            booked_slot = BookedSlots(
                email=email,
                date=selected_slot.date,
                time_start=selected_slot.time_start,
                time_end=selected_slot.time_end,
                link=common_meeting_link
            )
            booked_slot.save()


            # try:
            #     interviewlink = MeetingLink.objects.get(slot=selected_slot)
            #     interview_link = interviewlink.link
            # except MeetingLink.DoesNotExist:
            #     interview_link = None

            user_context = {
                'email': form.cleaned_data['email'],
                'slot': form.cleaned_data['slot'],
                'selected_slot_date': selected_slot.date.strftime("%Y-%m-%d"),
                'selected_slot_start_time': selected_slot.time_start.strftime("%I:%M %p"),
                'selected_slot_end_time': selected_slot.time_end.strftime("%I:%M %p"),
                'interview_link': common_meeting_link, 
                "current_year": current_year 
            }    
            user_html_content = render_to_string('emailbody.html', user_context)
            email_subject_user = 'Your Interview Slot Booking Confirmation'
            from_email = 'sauravkr.rathaur9@gmail.com'
            to_email = [email]
            
            user_msg = EmailMultiAlternatives(email_subject_user, '', from_email, to_email)
            user_msg.attach_alternative(user_html_content, "text/html")
            user_msg.send()


            return redirect("/")  # Redirect to a success page
    else:
        form = SlotBookingForm()

    return render(request, "slotbooking.html", {"form": form, 'time_slots': time_slots,"current_year": current_year})