# Generated by Django 4.0 on 2021-12-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_instrument_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='slug',
            field=models.SlugField(default=3, unique=True),
            preserve_default=False,
        ),
    ]
