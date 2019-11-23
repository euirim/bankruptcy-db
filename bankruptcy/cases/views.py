from django.shortcuts import render
from django.db.models import Q
from django.views.generic import DetailView

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet as DocViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import CaseDocument
from .models import Case, DocketEntry, Document
from .serializers import CaseSerializer, DocketEntrySerializer, DocumentSerializer, CaseDocumentSerializer


"""
def search(request):
    query_str = request.GET.get('q')
    cases = None
    if query_str:
        query_str = query_str.lower()
        cases = CaseDocument.search().query(
            'multi_match',
            query=query_str,
            fields=['name', 'jurisdiction']
        )[:30].to_queryset()

    return render(
        request,
        'cases/search.html',
        {'cases': cases, 'query': query_str}
    )
"""


class CaseDetail(DetailView):

    model = Case
    slug_field = "pk"
    slug_url_kwarg = "pk"


class CaseViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    @action(detail=False, methods=['post'])
    def search(self, request):
        query_str = request.data['query']
        if not query_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        query_str = query_str.lower()
        cases = CaseDocument.search().query(
            'multi_match',
            query=query_str,
            fields=['name', 'jurisdiction']
        ).to_queryset()

        return Response(cases)


class DocketEntryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DocketEntry.objects.all()
    serializer_class = DocketEntrySerializer


class DocumentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def list(self, request):
        query_str = request.GET.get('q')

        if not query_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cases = None
        query_str = query_str.lower()
        cases = CaseDocument.search().query(
            'multi_match',
            query=query_str,
            fields=['name', 'jurisdiction']
        )[:30].to_queryset()

        return Response(CaseSerializer(cases, many=True).data)


"""
    document = CaseDocument
    serializer_class = CaseDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        'name',
        'recap_id',
        'pacer_id',
        'jurisdiction',
        'chapter',
    )

    # Filter fields
    filter_fields = {}

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }

    # Specify default ordering
    ordering = ()
"""