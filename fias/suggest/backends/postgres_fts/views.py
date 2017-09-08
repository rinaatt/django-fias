from django.db import connections, OperationalError
from django.http import Http404, JsonResponse
from django.utils.encoding import smart_text
from django.views.generic.list import BaseListView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django_select2.views import AutoResponseView

from fias.models import AddrObj, AddrObjIndex


def dict_fetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class PostgresResponseView(AutoResponseView):
    term: str = None
    object_list: list = None
    widget = None

    def get(self, request, *args, **kwargs):
        """
        Return a :class:`.django.http.JsonResponse`.

        Example::

            {
                'results': [
                    {
                        'text': "foo",
                        'id': 123
                    }
                ],
                'more': true
            }

        """
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': obj['fullname'],
                    'id': obj['aoguid'],
                    # 'level': obj['aolevel']
                }
                for obj in context['object_list']
                ],
            'more': context['page_obj'].has_next()
        })

    def get_queryset(self):
        qs = AddrObjIndex.objects\
            .filter(search_vector=self.term)\
            .order_by('-item_weight')
        return qs.values('aoguid', 'fullname')[0:50]


class GetAreasListView(BaseListView):

    def get(self, request, *args, **kwargs):
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': smart_text(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
                ],
        })

    def get_queryset(self):
        try:
            address = AddrObj.objects.get(pk=self.term)
        except AddrObj.DoesNotExist:
            return []

        city = self._get_city_obj(address)

        if city is None:
            return []

        return AddrObj.objects.filter(parentguid=city.pk, shortname='р-н')

    def _get_city_obj(self, obj):
        if obj.shortname != 'г' and obj.aolevel > 1:
            parent = AddrObj.objects.get(pk=obj.parentguid)
            return self._get_city_obj(parent)
        elif obj.shortname == 'г':
            return obj
        else:
            return None
