from celery import shared_task
from django.core.cache import cache
from holders.documents import ShareholdersHistoryDocument
from elasticsearch_dsl.query import MultiMatch


@shared_task
def cache_search_results(query):
    es_query = MultiMatch(query=query, fields=["symbol"], fuzziness="AUTO")
    results = ShareholdersHistoryDocument.search().query(es_query)[:10000]

    serialized = [hit.to_dict() for hit in results]

    cache.set(f"search:{query}", serialized, timeout=600)
    return f"cached {len(serialized)} items for {query}"
