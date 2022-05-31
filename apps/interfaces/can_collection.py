from django.db import models


class CanCollection(models.Model):
    """能够被收藏的模型interface
    """
    class Meta:
        abstract = True
