# Generated by Django 5.2 on 2025-04-24 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='passed_from',
        ),
    ]
