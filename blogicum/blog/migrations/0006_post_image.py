# Generated by Django 3.2.16 on 2024-12-03 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20241118_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images', verbose_name='Фото'),
        ),
    ]
