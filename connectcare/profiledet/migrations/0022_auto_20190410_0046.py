# Generated by Django 2.0.1 on 2019-04-09 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiledet', '0021_auto_20190410_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='auth',
            field=models.TextField(blank=True, null=True),
        ),
    ]