# Generated by Django 3.0.5 on 2020-04-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease_option',
            name='license',
            field=models.FileField(blank=True, upload_to='lease_files'),
        ),
    ]
