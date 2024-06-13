# Generated by Django 5.0.3 on 2024-03-07 05:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=1000)),
                ('details', models.CharField(max_length=1000)),
                ('complaintimage', models.ImageField(upload_to='complaint')),
                ('complaintstatus', models.CharField(choices=[('Pending', 'Pending'), ('Action Taken', 'Action Taken'), ('Solved', 'Solved')], default='Pending', max_length=150)),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app3.usersignup')),
            ],
        ),
    ]