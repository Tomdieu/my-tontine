# Generated by Django 3.2.9 on 2022-01-15 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tontine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cotisation',
            name='creator',
        ),
    ]
