from django.db import models


class ShareholdersHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    date = models.DateField()
    shareholder_id = models.BigIntegerField()
    shareholder_shares = models.BigIntegerField()
    shareholder_percentage = models.FloatField()
    shareholder_instrument_id = models.CharField(max_length=50)
    shareholder_name = models.CharField(max_length=255)
    change = models.BigIntegerField()
    symbol = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.shareholder_id}"

    class Meta:
        managed = False
        db_table = 'ShareholdersHistory'
