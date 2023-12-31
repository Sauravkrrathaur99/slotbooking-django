# Generated by Django 4.2.5 on 2023-10-02 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slotbooking_app', '0011_meetinglink_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetinglink',
            name='user',
        ),
        migrations.AlterField(
            model_name='meetinglink',
            name='link',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='UserMeetingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slotbooking_app.meetinglink')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
