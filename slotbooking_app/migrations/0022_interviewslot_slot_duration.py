# Generated by Django 4.1.7 on 2023-10-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slotbooking_app', '0021_rename_bookedslot_bookedslots'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewslot',
            name='slot_duration',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
