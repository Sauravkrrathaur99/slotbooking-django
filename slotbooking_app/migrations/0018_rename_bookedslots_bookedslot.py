# Generated by Django 4.1.7 on 2023-10-02 06:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slotbooking_app', '0017_rename_bookedslot_bookedslots'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookedSlots',
            new_name='BookedSlot',
        ),
    ]
