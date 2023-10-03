
# views.py
import time
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from slotbooking_app.models import BookedSlots, InterviewSlot, MeetingLink
from .forms import SlotBookingForm
from django.core.mail import send_mail
import datetime
from django.contrib import messages
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
            slot_user = selected_slot.user
            selected_slot.is_booked = True
            selected_slot.save()
            # Create and save a new instance of BookedSlots
            booked_slot = BookedSlots(
                user=slot_user,
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
            from_email = 'onelogica.connect@gmail.com'
            to_email = [email]
            
            user_msg = EmailMultiAlternatives(email_subject_user, '', from_email, to_email)
            user_msg.attach_alternative(user_html_content, "text/html")
            user_msg.send()
            time.sleep(2)
            messages.success(request, 'Congratulations!! Your slot is booked, please check your email for details. All The Best !!')


            return redirect("/")  # Redirect to a success page
    else:
        form = SlotBookingForm()

    return render(request, "slotbooking.html", {"form": form, 'time_slots': time_slots,"current_year": current_year})