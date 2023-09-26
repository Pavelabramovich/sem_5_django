# Generated by Django 4.2.1 on 2023-08-05 20:49

from django.db import migrations, models
import apps.shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_profile_address_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='phone',
            field=models.CharField(help_text='Enter a phone in format +375 (29) XXX-XX-XX', max_length=64, validators=[apps.shop.validators.FullMatchRegexValidator('\\+375\\s*\\(\\s*29\\s*\\)\\s*(\\d{3})\\s*-\\s*(\\d{2})\\s*-\\s*(\\d{2})', 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.', code='invalid')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(help_text='Enter a phone in format +375 (29) XXX-XX-XX', max_length=64, validators=[apps.shop.validators.FullMatchRegexValidator('\\+375\\s*\\(\\s*29\\s*\\)\\s*(\\d{3})\\s*-\\s*(\\d{2})\\s*-\\s*(\\d{2})', 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.', code='invalid')]),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(help_text='Enter a phone in format +375 (29) XXX-XX-XX', max_length=64, validators=[apps.shop.validators.FullMatchRegexValidator('\\+375\\s*\\(\\s*29\\s*\\)\\s*(\\d{3})\\s*-\\s*(\\d{2})\\s*-\\s*(\\d{2})', 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.', code='invalid')]),
        ),
    ]
