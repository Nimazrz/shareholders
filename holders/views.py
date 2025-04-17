from django.shortcuts import render
from elasticsearch_dsl.query import MultiMatch
from .documents import ShareholdersHistoryDocument
import time
import redis
import json
from elasticsearch_dsl import connections

r = redis.StrictRedis(host="localhost", port=6379, db=0)


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
        hits = response["hits"]["hits"]
        if not hits:
            break
        all_hits.extend(hits)

    return all_hits


def index(request):
    q = request.GET.get("q")
    context = {"query": q}
    if q:
        start = time.time()
        cache_key = f"search:{q}"
        cached_result = r.get(cache_key)

        if cached_result:
            print("✅ Result from Redis cache")
            all_hits = json.loads(cached_result)
            context["shareholders"] = all_hits
            end = time.time()
            context["search_time"] = end - start
        else:
            print("🔍 Querying Elasticsearch...")
            query = MultiMatch(query=q, fields=["symbol"], fuzziness="AUTO")
            all_hits = get_all_hits(query)
            all_hits = [hit["_source"] for hit in all_hits]
            end = time.time()
            search_time = end - start
            context["shareholders"] = all_hits
            context["search_time"] = search_time

            r.setex(cache_key, 600, json.dumps(all_hits))

    return render(request, "index.html", context)
