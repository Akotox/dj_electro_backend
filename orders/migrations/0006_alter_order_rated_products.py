# Generated by Django 5.1 on 2024-09-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='rated_products',
            field=models.JSONField(default=list),
        ),
    ]
