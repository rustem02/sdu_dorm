# Generated by Django 5.0.2 on 2024-04-01 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_booking_semester_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=100)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defaultpayment', to='app.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defaultpayment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]