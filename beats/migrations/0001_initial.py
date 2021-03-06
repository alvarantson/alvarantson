# Generated by Django 3.0.5 on 2020-04-23 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=999, unique=True)),
                ('tags', models.TextField(blank=True)),
                ('img', models.ImageField(upload_to='beat_covers')),
                ('mp3', models.FileField(upload_to='beat_mp3s')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=999, unique=True)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lease_option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=999)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('file', models.FileField(upload_to='lease_files')),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beats.Beat')),
            ],
        ),
    ]
