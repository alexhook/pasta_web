# Generated by Django 3.2.8 on 2021-12-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(),
        ),
    ]