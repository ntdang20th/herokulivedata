# Generated by Django 4.1.2 on 2022-10-17 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livedata', '0003_alter_systemuser_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemuser',
            name='sur_name',
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='hospital_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]