# Generated by Django 4.1.2 on 2022-10-17 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_myuser_district_province_ward_delete_systemuser_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
