# Generated by Django 4.0 on 2021-12-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20211214_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='is_published',
            field=models.BooleanField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
