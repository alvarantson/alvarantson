# Generated by Django 3.0.5 on 2020-04-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_license_template_receipt_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(max_length=999)),
                ('seller_email', models.CharField(max_length=999)),
                ('website', models.CharField(max_length=999)),
            ],
        ),
    ]