# Generated by Django 5.2 on 2025-06-19 13:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_leave_status_alter_leave_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
