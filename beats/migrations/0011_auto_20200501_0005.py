# Generated by Django 3.0.5 on 2020-04-30 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0010_auto_20200430_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lease_option',
            old_name='file_url',
            new_name='dropbox_url',
        ),
    ]