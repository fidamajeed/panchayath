# Generated by Django 5.0.3 on 2024-03-07 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0006_alter_usersignup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='proof',
            field=models.ImageField(null=True, upload_to='proof'),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
