# Generated by Django 3.2.6 on 2021-08-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinebookingclass',
            name='ref_id',
            field=models.IntegerField(),
        ),
    ]