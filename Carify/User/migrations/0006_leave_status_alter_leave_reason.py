# Generated by Django 5.2 on 2025-06-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_customuser_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='leave',
            name='reason',
            field=models.TextField(),
        ),
    ]
