# Generated by Django 5.0.4 on 2024-07-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0004_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
