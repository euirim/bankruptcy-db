from django_elasticsearch_dsl_drf.serializers import DocumentSerializer as DocSerializer
from rest_framework import serializers

from .models import Case, DocketEntry, Document
from .documents import CaseDocument


class CaseSerializer(serializers.ModelSerializer):
    recap_url = serializers.SerializerMethodField('get_recap_url')

    def get_recap_url(self, obj):
        return f"https://www.courtlistener.com{obj.data['absolute_url']}"

    class Meta:
        model = Case
        fields = ['id', 'url', 'name', 'recap_id', 'pacer_id', 'date_filed', 'date_created', 'date_terminated',
                  'date_blocked', 'jurisdiction', 'chapter', 'docket_entries', 'recap_url',]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('text',)


class DocketEntrySerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = DocketEntry
        fields = ['id', 'url', 'recap_id', 'date_filed', 'date_created', 'description', 'case', 'documents']
        depth = 1


class CaseDocumentSerializer(DocSerializer):
    class Meta:
        document = CaseDocument
        exclude = ('text',)
