# Generated by Django 2.0.2 on 2018-03-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_auto_20180305_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]