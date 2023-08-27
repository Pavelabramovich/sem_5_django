# Generated by Django 4.2.1 on 2023-08-27 17:05

import apps.core.media_tools.storages
import apps.core.model_tools.named_image_field
import apps.core.model_tools.svg_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_delete_provider_provider_alter_product_providers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'permissions': (('provide_product', 'Can provide products'),)},
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=apps.core.model_tools.named_image_field.NamedImageField(blank=True, storage=apps.core.media_tools.storages.OverwriteCodedStorage(), upload_to='categories_images'),
        ),
        migrations.AddField(
            model_name='category',
            name='logo',
            field=apps.core.model_tools.svg_field.SvgField(default='categories_logo/logo_default.svg', storage=apps.core.media_tools.storages.OverwriteCodedStorage(), upload_to='categories_logo', validators=[apps.core.model_tools.svg_field.validate_svg, apps.core.model_tools.svg_field.validate_svg]),
        ),
    ]