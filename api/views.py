from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from holders.documents import ShareholdersHistoryDocument
from .serializers import ShareholdersHistoryDocumentSerializer
from django_elasticsearch_dsl_drf.filter_backends import (FilteringFilterBackend, CompoundSearchFilterBackend)


class ShareholdersHistoryDocumentView(DocumentViewSet):
    document = ShareholdersHistoryDocument
    serializer_class = ShareholdersHistoryDocumentSerializer
    filter_backends = [FilteringFilterBackend, CompoundSearchFilterBackend]
    search_fields = ('symbol',)
    filter_fields = {
        'symbol': 'symbol.raw',
        'date': 'date',
    }