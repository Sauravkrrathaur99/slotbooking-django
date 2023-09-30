# from django.contrib import admin
# from .models import InterviewSlot

# admin.site.register(InterviewSlot)



from django.contrib import admin
from .models import BookedSlots, InterviewSlot
from .models import MeetingLink
import csv
from django.http import HttpResponse
from django.utils.html import format_html


class InterviewSlotAdmin(admin.ModelAdmin):
    list_display = ('formatted_datetime', 'is_booked')

    def formatted_datetime(self, obj):
        return f'{obj.date.strftime("%Y-%m-%d")} {obj.time_start.strftime("%I:%M %p")} - {obj.time_end.strftime("%I:%M %p")}'

    formatted_datetime.short_description = 'Date and Time'

class MeetingLinkAdmin(admin.ModelAdmin):
    list_display = ('link',)


class BookedSlotsAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'time_start', 'time_end', 'formatted_link')
    list_filter = ('date',)
    search_fields = ('email',)
    actions = ['export_as_csv']

    def formatted_link(self, obj):
        link = obj.link if obj.link else "No Link Available"
        if obj.link:
            return format_html('<a href="{}" target="_blank">Click here to join</a>', link)

        return "No Link Available"

    formatted_link.short_description = 'Link'
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="booked_slots.csv"'

        writer = csv.writer(response)
        writer.writerow(['Email', 'Date', 'Start Time', 'End Time', 'Link'])

        for slot in queryset:
            writer.writerow([slot.email, slot.date, slot.time_start, slot.time_end, slot.link])

        return response

    export_as_csv.short_description = 'Export selected as CSV'


admin.site.register(InterviewSlot, InterviewSlotAdmin)
admin.site.register(MeetingLink, MeetingLinkAdmin)
admin.site.register(BookedSlots, BookedSlotsAdmin)