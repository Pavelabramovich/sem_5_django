# Generated by Django 4.2.1 on 2023-07-25 22:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0009_alter_provider_address_alter_provider_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='address',
            field=models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('\\+375\\s*\\(\\s*29\\s*\\)\\s*\\d{3}\\s*-\\s*\\d{2}\\s*-\\s*\\d{2}', 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.', code='invalid')]),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(max_length=64),
        ),
    ]