# Generated by Django 3.2.3 on 2021-05-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountconnection',
            name='button_url',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='accountconnection',
            name='code',
            field=models.CharField(max_length=10000),
        ),
    ]
