# Generated by Django 3.0.5 on 2020-04-28 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yt_link', models.CharField(max_length=999)),
                ('role', models.CharField(blank=True, max_length=999)),
            ],
        ),
    ]
