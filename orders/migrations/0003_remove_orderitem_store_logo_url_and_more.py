# Generated by Django 5.1 on 2024-09-04 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitem_product_id_alter_orderitem_store_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='store_logo_url',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='store_title',
        ),
    ]
