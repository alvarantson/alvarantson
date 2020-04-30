# Generated by Django 3.0.5 on 2020-04-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0006_auto_20200425_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease_option',
            name='file_url',
            field=models.CharField(blank=True, max_length=999),
        ),
        migrations.AlterField(
            model_name='lease_option',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='lease_files'),
        ),
    ]
