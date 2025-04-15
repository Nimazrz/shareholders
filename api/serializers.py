from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from holders.documents import ShareholdersHistoryDocument


class ShareholdersHistoryDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ShareholdersHistoryDocument
        fields = '__all__'

