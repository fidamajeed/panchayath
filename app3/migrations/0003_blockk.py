# Generated by Django 5.0.3 on 2024-03-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0002_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='blockk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panchayatname', models.CharField(max_length=100)),
                ('wards', models.IntegerField()),
            ],
        ),
    ]