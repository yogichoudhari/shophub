# Generated by Django 3.0 on 2022-10-24 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20221024_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discription',
        ),
        migrations.AlterField(
            model_name='product',
            name='gender_category',
            field=models.CharField(choices=[('None', 'None'), ('Men', 'Men'), ('Women', 'Women')], default=None, max_length=30, null=True),
        ),
    ]
