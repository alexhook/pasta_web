# Generated by Django 4.0 on 2021-12-11 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_alter_instrument_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cuisine',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]
