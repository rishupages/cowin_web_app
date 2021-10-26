# Generated by Django 3.2.6 on 2021-08-27 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_vaccinebookingclass_ref_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('city', models.CharField(max_length=50)),
                ('pin_code', models.IntegerField()),
                ('total_vaccine', models.IntegerField()),
                ('available_vaccine', models.IntegerField()),
            ],
            options={
                'db_table': 'vaccineslot',
            },
        ),
    ]