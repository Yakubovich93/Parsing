# Generated by Django 3.1.2 on 2020-11-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
    ]
