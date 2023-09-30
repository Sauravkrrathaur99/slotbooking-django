from django.db import models


class InterviewSlot(models.Model):
    date = models.DateField(null=True, blank=False)
    time_start = models.TimeField(null=True, blank=False)
    time_end = models.TimeField(null=True, blank=False)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.date.strftime("%Y-%m-%d")} {self.time_start.strftime("%I:%M %p")} - {self.time_end.strftime("%I:%M %p")}'


class MeetingLink(models.Model):
    link = models.TextField(null=True)


class BookedSlots(models.Model):
    email = models.EmailField(null=True)
    date = models.DateField(null=True, blank=False)
    time_start = models.TimeField(null=True, blank=False)
    time_end = models.TimeField(null=True, blank=False)
    link = models.TextField(null=True)