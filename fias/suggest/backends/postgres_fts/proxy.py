from django.db import models
from django.contrib.postgres.search import SearchQuery as SearchQueryOrig
from fias.models import AddrObjIndex


class SearchQuery(SearchQueryOrig):

    def as_sql(self, compiler, connection):
        params = [self.value]
        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = 'to_tsquery({}::regconfig, %s)'.format(config_sql)
            params = config_params + [self.value]
        else:
            template = 'to_tsquery(%s)'
        if self.invert:
            template = '!!({})'.format(template)
        return template, params


class AddrObjIndexSearchQuerySet(models.QuerySet):

    def term(self, words: str):
        if not words:
            qs = self.filter(aolevel=1).order_by('-item_weight')
        else:
            if len(words.split()) > 1:
                words = words.lower().translate(str.maketrans('.,;', '   '))
                words_query = ' & '.join(w+':*' for w in words.split() if w)
            else:
                words_query = words.lower().strip() + ':*'
            qs = self.filter(search_vector=SearchQuery(words_query,
                                                       config='russian'))
        return qs.order_by('-item_weight')


class AddrObjIndexProxy(AddrObjIndex):

    class Meta:
        proxy = True

    search = AddrObjIndexSearchQuerySet.as_manager()
