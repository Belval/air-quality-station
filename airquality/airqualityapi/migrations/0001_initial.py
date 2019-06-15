# Generated by Django 2.2.2 on 2019-06-15 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('pm25', models.DecimalField(decimal_places=10, max_digits=10)),
                ('pm10', models.DecimalField(decimal_places=10, max_digits=10)),
            ],
        ),
    ]
