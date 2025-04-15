from django.shortcuts import render, get_object_or_404
from elasticsearch_dsl.query import MultiMatch
from .documents import ShareholdersHistoryDocument
from .models import ShareholdersHistory
from elasticsearch_dsl import connections
import time


def get_all_hits(query, scroll="2m", batch_size=10000):
    client = connections.get_connection()
    index = ShareholdersHistoryDocument._index._name

    response = client.search(
        index=index,
        body={"query": query.to_dict()},
        scroll=scroll,
        size=batch_size,
    )

    scroll_id = response["_scroll_id"]
    hits = response["hits"]["hits"]
    all_hits = hits.copy()

    while True:
        response = client.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = response["_scroll_id"]
        hits = response["hits"]["hits"]
        if not hits:
            break
        all_hits.extend(hits)

    return all_hits


def index(request):
    q = request.GET.get("q")
    context = {'query': q}
    if q:
        start = time.time()
        query = MultiMatch(query=q, fields=["symbol"], fuzziness="AUTO")
        all_hits = get_all_hits(query)
        end = time.time()
        print(end - start)
        context["shareholders"] = [hit["_source"] for hit in all_hits]
    return render(request, "index.html", context)


