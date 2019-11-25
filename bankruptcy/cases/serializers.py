from django_elasticsearch_dsl_drf.serializers import DocumentSerializer as DocSerializer
from rest_framework import serializers

from .models import Case, DocketEntry, Document
from .documents import CaseDocument


class CaseSerializer(serializers.ModelSerializer):
    docket_entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'name', 'recap_id', 'pacer_id', 'date_filed', 'date_created', 'date_terminated',
                  'date_blocked', 'jurisdiction', 'chapter', 'docket_entries']


class DocketEntrySerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DocketEntry
        fields = ['id', 'recap_id', 'date_filed', 'date_created', 'description', 'case', 'documents']
        depth = 2


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class CaseDocumentSerializer(DocSerializer):
    class Meta:
        document = CaseDocument
        fields = '__all__'
