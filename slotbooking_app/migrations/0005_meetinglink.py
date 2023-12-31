# Generated by Django 4.1.7 on 2023-09-30 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slotbooking_app', '0004_remove_interviewslot_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('slot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='slotbooking_app.interviewslot')),
            ],
        ),
    ]
