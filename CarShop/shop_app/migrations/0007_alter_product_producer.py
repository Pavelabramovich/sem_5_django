# Generated by Django 4.2.1 on 2023-07-25 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0006_alter_provider_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop_app.producer'),
        ),
    ]