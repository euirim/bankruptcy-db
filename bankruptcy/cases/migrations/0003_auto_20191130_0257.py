# Generated by Django 2.2.6 on 2019-11-30 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_auto_20191130_0251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='keywords',
            new_name='entities',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='keywords',
            new_name='entities',
        ),
        migrations.AddField(
            model_name='case',
            name='recap_url',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
