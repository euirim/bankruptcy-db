from django.db import models
from django.contrib.postgres.fields import JSONField

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, Tag
from easy_thumbnails.fields import ThumbnailerImageField


class PersonTagged(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class OrgTagged(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class Case(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    recap_id = models.IntegerField()
    pacer_id = models.CharField(max_length=50, db_index=True)
    date_filed = models.DateField(db_index=True, blank=True, null=True)
    date_created = models.DateField(db_index=True)
    date_terminated = models.DateField(db_index=True, blank=True, null=True)
    date_blocked = models.DateField(db_index=True, blank=True, null=True)
    jurisdiction = models.CharField(max_length=50)
    chapter = models.SmallIntegerField(
        db_index=True,
        blank=True,
        null=True
    )
    recap_url = models.CharField(max_length=2048, blank=True, null=True)
    entities = TaggableManager()
    people = TaggableManager(through=PersonTagged, related_name="person_cases")
    organizations = TaggableManager(through=OrgTagged, related_name="org_cases")
    data = JSONField()

    def __str__(self):
        return self.name


class DocketEntry(models.Model):
    recap_id = models.IntegerField()
    date_filed = models.DateField(db_index=True, blank=True, null=True)
    date_created = models.DateField(db_index=True)
    description = models.TextField(blank=True, null=True)
    case = models.ForeignKey(
        'Case',
        on_delete=models.CASCADE,
        related_name='docket_entries'
    )

    def __str__(self):
        return str(self.recap_id)


class Document(models.Model):
    recap_id = models.IntegerField()
    pacer_id = models.CharField(max_length=50, db_index=True)
    doc_type = models.CharField(max_length=50)
    is_sealed = models.BooleanField()
    is_available = models.BooleanField()
    file_url = models.URLField(blank=True, null=True, max_length=2048)
    description = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    docket_entry = models.ForeignKey(
        'DocketEntry',
        on_delete=models.CASCADE,
        related_name='documents'
    )
    preview = ThumbnailerImageField(upload_to='doc_previews', blank=True)
    entities = TaggableManager()
    people = TaggableManager(through=PersonTagged, related_name="person_docs")
    organizations = TaggableManager(through=OrgTagged, related_name="org_docs")

    def __str__(self):
        return self.pacer_id
