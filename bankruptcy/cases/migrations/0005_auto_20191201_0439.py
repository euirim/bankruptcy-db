# Generated by Django 2.2.6 on 2019-12-01 04:39

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('cases', '0004_remove_case_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonTagged',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases_persontagged_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases_persontagged_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrgTagged',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases_orgtagged_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases_orgtagged_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='document',
            name='organizations',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='org_docs', through='cases.OrgTagged', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='document',
            name='people',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='person_docs', through='cases.PersonTagged', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
