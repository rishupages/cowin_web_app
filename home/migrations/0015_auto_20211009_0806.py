# Generated by Django 3.2.6 on 2021-10-09 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_vaccinebookingclass_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccineslot',
            name='pin_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vaccineslot',
            name='vaccine_12',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vaccineslot',
            name='vaccine_18',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vaccineslot',
            name='vaccine_45',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vaccineslot',
            name='vaccine_60',
            field=models.IntegerField(),
        ),
    ]
