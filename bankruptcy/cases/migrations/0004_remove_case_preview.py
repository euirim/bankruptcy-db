# Generated by Django 2.2.6 on 2019-12-01 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_auto_20191130_0257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='preview',
        ),
    ]
