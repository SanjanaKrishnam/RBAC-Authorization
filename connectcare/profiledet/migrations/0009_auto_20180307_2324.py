# Generated by Django 2.0.2 on 2018-03-07 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiledet', '0008_auto_20180307_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='qual',
            field=models.CharField(blank=True, default='NONO', max_length=255),
        ),
    ]
