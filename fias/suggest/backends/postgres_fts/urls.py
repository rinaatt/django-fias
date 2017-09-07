# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^suggest.json$', v.PostgresResponseView.as_view(),
        name='suggest'),
    url(r'^suggest-area.json$', v.GetAreasListView.as_view(),
        name='suggest-area'),
]
