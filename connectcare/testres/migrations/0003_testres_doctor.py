# Generated by Django 2.0.2 on 2018-03-10 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testres', '0002_testres_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='testres',
            name='doctor',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
