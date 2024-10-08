# Generated by Django 5.1 on 2024-09-05 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_alter_storeorder_order_reference_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeorder',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('processing', 'Processing'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
    ]
