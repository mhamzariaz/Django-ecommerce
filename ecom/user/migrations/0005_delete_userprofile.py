# Generated by Django 4.1 on 2022-09-08 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_order_address_remove_order_products_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
