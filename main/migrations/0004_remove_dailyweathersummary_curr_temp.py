# Generated by Django 5.1.2 on 2024-10-20 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_dailyweathersummary_curr_temp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyweathersummary',
            name='curr_temp',
        ),
    ]
