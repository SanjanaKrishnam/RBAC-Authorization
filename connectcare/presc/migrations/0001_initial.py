# Generated by Django 2.0.3 on 2018-03-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Presc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.CharField(max_length=255)),
                ('patient', models.CharField(max_length=255)),
                ('medicine', models.CharField(max_length=255)),
                ('Notes', models.CharField(max_length=10000)),
            ],
        ),
    ]
