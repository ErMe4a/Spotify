# Generated by Django 3.2 on 2022-09-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_rename_performer_music_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
