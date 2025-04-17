from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from holders.documents import ShareholdersHistoryDocument
from .serializers import ShareholdersHistoryDocumentSerializer
from .tasks import cache_search_results
import time
from django.core.cache import cache


class ShareholdersHistoryDocumentView(DocumentViewSet):
    document = ShareholdersHistoryDocument
    serializer_class = ShareholdersHistoryDocumentSerializer
    filter_backends = [FilteringFilterBackend, CompoundSearchFilterBackend]
    search_fields = ('symbol',)
    filter_fields = {
        'symbol': 'symbol.raw',
        'date': 'date',
    }

    def filter_queryset(self, queryset):
        query = self.request.query_params.get('q')
        if query:
            stat = time.time()
            key = f'search:{query}'

            if not cache.get(key):
                print(f"⏳ Not found in cache. Caching '{query}'...")
                cache_search_results.delay(query)
                end = time.time()
                print(f"⏱️ Celery task queued {end - stat} seconds")
            else:
                end = time.time()
                print(end - stat)
                print(f"✅ Found in cache: '{query}'")

        return super().filter_queryset(queryset)
