# Generated by Django 3.1.6 on 2021-03-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20210307_0246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]