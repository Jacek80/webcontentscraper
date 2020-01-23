from django.db import models


class StoredWebPages(models.Model):
    address = models.CharField(max_length=128, null=False)
    text_length = models.IntegerField(default=0)
    images_number = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def get_non_field(self):
        return 'stuff'