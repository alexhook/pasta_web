# Generated by Django 4.0 on 2022-01-24 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientgroup',
            options={'verbose_name': 'Группа ингредиентов', 'verbose_name_plural': 'Группы ингредиентов'},
        ),
        migrations.AlterModelOptions(
            name='instrument',
            options={'verbose_name': 'Инструмент', 'verbose_name_plural': 'Инструменты'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.ingredientgroup', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='image',
            field=models.ImageField(upload_to='wiki/ingredients/', verbose_name='Иллюстрация'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='ingredientgroup',
            name='image',
            field=models.ImageField(upload_to='wiki/ingredientgroups/', verbose_name='Иллюстрация'),
        ),
        migrations.AlterField(
            model_name='ingredientgroup',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='image',
            field=models.ImageField(upload_to='wiki/instruments/', verbose_name='Иллюстрация'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Наименование'),
        ),
    ]