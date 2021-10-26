# Generated by Django 3.2.6 on 2021-09-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210901_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member_info_Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('uid', models.IntegerField()),
                ('total_member', models.IntegerField()),
                ('age', models.IntegerField()),
                ('first_booking', models.DateField()),
                ('second_booking', models.DateField()),
            ],
            options={
                'db_table': 'member_info_table',
            },
        ),
        migrations.RenameField(
            model_name='vaccinebookingclass',
            old_name='first_booking',
            new_name='first_dose',
        ),
        migrations.RenameField(
            model_name='vaccinebookingclass',
            old_name='second_booking',
            new_name='second_dose',
        ),
        migrations.RemoveField(
            model_name='vaccinebookingclass',
            name='age',
        ),
        migrations.RemoveField(
            model_name='vaccinebookingclass',
            name='total_member',
        ),
        migrations.AddField(
            model_name='vaccinebookingclass',
            name='city',
            field=models.CharField(default='null', max_length=50),
        ),
        migrations.AddField(
            model_name='vaccinebookingclass',
            name='first_verification',
            field=models.BooleanField(default='null'),
        ),
        migrations.AddField(
            model_name='vaccinebookingclass',
            name='second_verification',
            field=models.BooleanField(default='null'),
        ),
        migrations.AlterField(
            model_name='vaccinebookingclass',
            name='phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vaccinebookingclass',
            name='uid',
            field=models.IntegerField(),
        ),
        migrations.AlterModelTable(
            name='vaccinebookingclass',
            table='vaccine_booking_info',
        ),
    ]