from django.shortcuts import render, get_object_or_404
from elasticsearch_dsl.query import MultiMatch
from .documents import ShareholdersHistoryDocument
from .models import ShareholdersHistory


def index(request):
    q = request.GET.get("q")
    context = {}
    if q:
        query = MultiMatch(query=q, fields=["shareholder_name", "shareholder_instrument_id"], fuzziness="AUTO")
        search = ShareholdersHistoryDocument.search().query(query)[0:10]
        response = search.execute()
        context["shareholders"] = response.hits
        print(context["shareholders"])
        for hit in response.hits:
            print(hit.meta.id)
            print(hit.shareholder_name)
            print(hit.__dict__)
    return render(request, "index.html", context)


def shareholder_detail(request,shareholderid):
    shareholder = get_object_or_404(ShareholdersHistory, id=shareholderid)
    return render(request, 'detail.html', {'shareholder': shareholder})

