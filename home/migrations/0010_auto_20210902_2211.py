# Generated by Django 3.2.6 on 2021-09-02 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_member_info_class_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinebookingclass',
            name='first_verification',
            field=models.BooleanField(default='False'),
        ),
        migrations.AlterField(
            model_name='vaccinebookingclass',
            name='second_verification',
            field=models.BooleanField(default='False'),
        ),
    ]
