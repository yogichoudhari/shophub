# Generated by Django 3.0 on 2022-10-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='Zip_code',
            new_name='zip_code',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='selling_price',
            new_name='actual_price',
        ),
        migrations.AddField(
            model_name='product',
            name='discounted_price',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='gender_category',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women')], default=None, max_length=30, null=True),
        ),
    ]
