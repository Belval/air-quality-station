# Generated by Django 2.2.2 on 2019-06-15 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airqualityapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='pm10',
            field=models.DecimalField(decimal_places=4, max_digits=16),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pm25',
            field=models.DecimalField(decimal_places=4, max_digits=16),
        ),
    ]