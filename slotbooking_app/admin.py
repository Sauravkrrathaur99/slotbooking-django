from django.contrib import admin
from .models import BookedSlots, InterviewSlot
from .models import MeetingLink
import csv
from django.template.loader import render_to_string
import time
from django.http import HttpResponse
from django.utils.html import format_html
from datetime import datetime, timedelta
import datetime
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives


# Change the site header to "Interview Slot Booking App"
admin.site.site_header = "Interview Slot Booking App"



# class InterviewSlotAdmin(admin.ModelAdmin):
#     list_display = ('formatted_datetime', 'is_booked',)

#     def get_list_display(self, request):
#         # Check if the logged-in user is a superuser or staff
#         if request.user.is_superuser:
#             return super().get_list_display(request) + ('user',)
#         return super().get_list_display(request)

#     def formatted_datetime(self, obj):
#         return f'{obj.date.strftime("%Y-%m-%d")} {obj.time_start.strftime("%I:%M %p")} - {obj.time_end.strftime("%I:%M %p")}'
#     formatted_datetime.short_description = 'Date and Time'

#     def get_form(self, request, obj=None, **kwargs):
#         # Automatically populate the user field with the logged-in user
#         form = super().get_form(request, obj, **kwargs)
#         form.base_fields['user'].initial = request.user
#         return form
    

#     def save_model(self, request, obj, form, change):
#         # Automatically populate the user field with the logged-in user
#         obj.user = request.user

#         # Create slots based on user-defined start time, end time, and slot duration
#         slot_duration_minutes = form.cleaned_data.get('slot_duration')
#         start_time = datetime.combine(obj.date, form.cleaned_data.get('time_start'))
#         end_time = datetime.combine(obj.date, form.cleaned_data.get('time_end'))

#         current_time = start_time
#         while current_time < end_time:
#             interview_slot = InterviewSlot(
#                 user=obj.user,
#                 date=obj.date,
#                 time_start=current_time.time(),
#                 time_end=(current_time + timedelta(minutes=slot_duration_minutes)).time(),
#             )
#             interview_slot.save()
#             current_time += timedelta(minutes=slot_duration_minutes)

#         super().save_model(request, obj, form, change)


    
#     def get_queryset(self, request):
#         # Filter interview slots based on the logged-in user
#         queryset = super().get_queryset(request)
#         if request.user.is_superuser:
#             return queryset
#         return queryset.filter(user=request.user)
    


    

    # def save_model(self, request, obj, form, change):
    #     # Automatically populate the user field with the logged-in user
    #     obj.user = request.user

    #     # Calculate the end time for each slot based on slot duration
    #     slot_duration_minutes = obj.slot_duration
    #     start_datetime = timezone.make_aware(
    #         timezone.datetime.combine(obj.date, obj.time_start)
    #     )
    #     end_datetime = timezone.make_aware(
    #         timezone.datetime.combine(obj.date, obj.time_end)
    #     )

    #     current_datetime = start_datetime
    #     while current_datetime < end_datetime:
    #         time_end = current_datetime + timedelta(minutes=slot_duration_minutes)
    #         interview_slot = InterviewSlot(
    #             user=obj.user,
    #             date=obj.date,
    #             time_start=current_datetime.time(),
    #             time_end=time_end.time(),
    #             slot_duration=obj.slot_duration,
    #         )
    #         interview_slot.save()
    #         current_datetime = time_end

    #     super().save_model(request, obj, form, change)
    
class InterviewSlotAdmin(admin.ModelAdmin):
    list_display = ('formatted_datetime', 'is_booked',)

    def get_list_display(self, request):
        # Check if the logged-in user is a superuser or staff
        if request.user.is_superuser:
            return super().get_list_display(request) + ('user',)
        return super().get_list_display(request)

    def formatted_datetime(self, obj):
        return f'{obj.date.strftime("%Y-%m-%d")} {obj.time_start.strftime("%I:%M %p")} - {obj.time_end.strftime("%I:%M %p")}'
    formatted_datetime.short_description = 'Date and Time'

    def get_form(self, request, obj=None, **kwargs):
        # Automatically populate the user field with the logged-in user
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        # Automatically populate the user field with the logged-in user
        obj.user = request.user

        # Calculate the end time for each slot based on slot duration
        slot_duration_minutes = obj.slot_duration
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(obj.date, obj.time_start)
        )
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(obj.date, obj.time_end)
        )
        print("end_datetime ", end_datetime)

        current_datetime = start_datetime
        while current_datetime < end_datetime:  
            time_end = current_datetime + timedelta(minutes=slot_duration_minutes)
            interview_slot = InterviewSlot(
                user=obj.user,
                date=obj.date,
                time_start=current_datetime.time(),
                time_end=time_end.time(),
                slot_duration=obj.slot_duration,
            )
            print("intervie" , interview_slot)
            interview_slot.save()
            current_datetime = time_end

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Filter interview slots based on the logged-in user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)
    




class MeetingLinkAdmin(admin.ModelAdmin):
    list_display = ('link',)

    def get_list_display(self, request):
        # Check if the logged-in user is a superuser or staff
        if request.user.is_superuser:
            return super().get_list_display(request) + ('user',)
        return super().get_list_display(request)

    def get_form(self, request, obj=None, **kwargs):
        # Automatically populate the user field with the logged-in user
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    def get_queryset(self, request):
        # Filter meeting links based on the logged-in user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)


class BookedSlotsAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'time_start', 'time_end', 'formatted_link',)
    list_filter = ('date',)
    search_fields = ('email',)
    actions = ['export_as_csv']

    def get_list_display(self, request):
        # Check if the logged-in user is a superuser or staff
        if request.user.is_superuser:
            return super().get_list_display(request) + ('user',)
        return super().get_list_display(request)

    def get_form(self, request, obj=None, **kwargs):
        # Automatically populate the user field with the logged-in user
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    def formatted_link(self, obj):
        link = obj.link if obj.link else "No Link Available"
        if obj.link:
            return format_html('<a href="{}" target="_blank">Click here to join</a>', link)

        return "No Link Available"

    formatted_link.short_description = 'Link'

    def get_queryset(self, request):
        # Filter booked slots based on the logged-in user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="booked_slots.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Date', 'Start Time', 'End Time', 'Link'])
        for slot in queryset:
            writer.writerow([slot.email, slot.date, slot.time_start, slot.time_end, slot.link])

        return response

    export_as_csv.short_description = 'Export selected as CSV'

    def save_model(self, request, obj, form, change):
        # Save the booked slot
        super().save_model(request, obj, form, change)
        current_year = datetime.datetime.now().year
        # Send an email confirmation
        user_context = {
            'email': obj.email,
            'slot': obj.date.strftime("%Y-%m-%d"),
            'selected_slot_start_time': obj.time_start.strftime("%I:%M %p"),
            'selected_slot_end_time': obj.time_end.strftime("%I:%M %p"),
            'interview_link': obj.link,
            "current_year": current_year 
        }
        user_html_content = render_to_string('emailbody.html', user_context)
        email_subject_user = 'Your Interview Slot Booking Confirmation'
        from_email = 'saurav.rathaur@onelogica.com'
        to_email = [obj.email]

        user_msg = EmailMultiAlternatives(email_subject_user, '', from_email, to_email)
        user_msg.attach_alternative(user_html_content, "text/html")
        user_msg.send()

admin.site.register(InterviewSlot, InterviewSlotAdmin)
admin.site.register(MeetingLink, MeetingLinkAdmin)
admin.site.register(BookedSlots, BookedSlotsAdmin)
