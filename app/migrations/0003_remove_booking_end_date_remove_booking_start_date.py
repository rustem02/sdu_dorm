# Generated by Django 5.0.2 on 2024-03-24 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_submissiondocuments_admin_comments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_date',
        ),
    ]
