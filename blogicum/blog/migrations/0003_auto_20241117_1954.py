# Generated by Django 3.2.16 on 2024-11-17 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_is_pulished_post_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='location',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации'),
        ),
    ]