from django.core.cache import cache
from elasticsearch_dsl.query import MultiMatch
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from holders.documents import ShareholdersHistoryDocument
from .serializers import ShareholdersHistoryDocumentSerializer
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, CompoundSearchFilterBackend
from rest_framework.response import Response
import time


class ShareholdersHistoryDocumentView(DocumentViewSet):
    document = ShareholdersHistoryDocument
    serializer_class = ShareholdersHistoryDocumentSerializer
    filter_backends = [FilteringFilterBackend, CompoundSearchFilterBackend]
    search_fields = ('symbol',)
    filter_fields = {
        'symbol': 'symbol.raw',
        'date': 'date',
    }

    def list(self, request, *args, **kwargs):
        query = request.query_params.get("q")
        if not query:
            return super().list(request, *args, **kwargs)

        cache_key = f"search:{query}"
        start = time.time()
        cached_result = cache.get(cache_key)

        if cached_result:
            end = time.time()
            return Response({
                "query": query,
                "count": len(cached_result),
                "results": cached_result,
                "search_time": end - start
            })
        else:
            es_query = MultiMatch(query=query, fields=["symbol"], fuzziness="AUTO")
            search = ShareholdersHistoryDocument.search().query(es_query)[:10000]
            hits = [hit.to_dict() for hit in search]

            cache.set(cache_key, hits, timeout=600)
            end = time.time()
            return Response({
                "query": query,
                "count": len(hits),
                "results": hits,
                "search_time": end - start
            })