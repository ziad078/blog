# Generated by Django 5.1.5 on 2025-02-10 16:26

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, default='photos/blanck.png', null=True, upload_to=accounts.models.to_path),
        ),
    ]
