# Generated by Django 5.1.5 on 2025-02-05 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='no_of_comments',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
