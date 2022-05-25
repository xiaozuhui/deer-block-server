from django.db import models


class Share(models.Model):
    """用于分享的模型，该模型是不是能用于别的app
    """
    pass


class Collection(models.Model):
    pass


class ThumbUp(models.Model):
    pass


class Tag(models.Model):
    pass

class Category(models.Model):
    pass