# Generated by Django 3.2.2 on 2022-10-31 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20221027_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(default='none', max_length=10),
        ),
    ]