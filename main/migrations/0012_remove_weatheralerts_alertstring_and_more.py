# Generated by Django 5.1.2 on 2024-10-20 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_weatheralerts_alertstring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatheralerts',
            name='alertstring',
        ),
        migrations.AddField(
            model_name='weatheralerts',
            name='delete_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weatheralerts',
            name='weatherstring',
            field=models.CharField(default=None, max_length=500),
        ),
    ]