# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.postgres.search import SearchVectorField

from ..fields import UUIDField
from ..apps import APP_LABEL


class AddrObjIndex(models.Model):

    class Meta:
        app_label = APP_LABEL

    aoguid = UUIDField()
    aolevel = models.PositiveSmallIntegerField()
    scname = models.TextField()
    fullname = models.TextField()
    item_weight = models.PositiveSmallIntegerField(default=64)
    search_vector = SearchVectorField(editable=False, null=True)
