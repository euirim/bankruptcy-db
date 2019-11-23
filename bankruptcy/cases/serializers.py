from django_elasticsearch_dsl_drf.serializers import DocumentSerializer as DocSerializer
from rest_framework import serializers

from .models import Case, DocketEntry, Document
from .documents import CaseDocument


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


class DocketEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocketEntry
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class CaseDocumentSerializer(DocSerializer):
    class Meta:
        document = CaseDocument
        fields = '__all__'
