from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import ShareholdersHistory


@registry.register_document
class ShareholdersHistoryDocument(Document):
    class Index:
        name = 'shareholders_history'
        settings = {'number_of_shards': 2, 'number_of_replicas': 0}

    class Django:
        model = ShareholdersHistory
        fields = [
            'symbol',
            'shareholder_name',
            'shareholder_instrument_id',
            'shareholder_id',
            'shareholder_percentage',
            'shareholder_shares',
            'date',
            'change',
        ]
