# Generated by Django 3.0.5 on 2020-05-04 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='the_stu',
            field=models.FileField(blank=True, null=True, upload_to='contact'),
        ),
        migrations.AlterField(
            model_name='about',
            name='mugshot',
            field=models.FileField(blank=True, null=True, upload_to='contact'),
        ),
    ]
