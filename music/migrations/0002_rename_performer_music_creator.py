# Generated by Django 3.2 on 2022-09-09 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='performer',
            new_name='creator',
        ),
    ]
