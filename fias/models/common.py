# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from ..fields import UUIDField
from ..app import APP_LABEL

__all__ = ['Common', 'June2016Update']


class Common(models.Model):

    class Meta:
        app_label = APP_LABEL
        abstract = True

    ifnsfl = models.CharField('Код ИФНС ФЗ', max_length=4, blank=True, null=True)
    terrifnsfl = models.CharField('Код территориального участка ИФНС ФЛ', max_length=4, blank=True, null=True)
    ifnsul = models.CharField('Код ИФНС ЮЛ', max_length=4, blank=True, null=True)
    terrifnsul = models.CharField('Код территориального участка ИФНС ЮЛ', max_length=4, blank=True, null=True)

    okato = models.CharField('ОКАТО', max_length=11, blank=True, null=True)
    oktmo = models.CharField('ОКТМО', max_length=11, blank=True, null=True)

    postalcode = models.CharField('Почтовый индекс', max_length=6, blank=True, null=True)

    updatedate = models.DateField('Дата время внесения записи')
    startdate = models.DateField('Начало действия записи')
    enddate = models.DateField('Окончание действия записи')
    normdoc = UUIDField('Внешний ключ на нормативный документ', blank=True, null=True)


class June2016Update(Common):

    class Meta:
        abstract = True

    cadnum = models.CharField('Кадастровый номер', max_length=100, blank=True, null=True)
    divtype = models.CharField('Тип адресации', max_length=1, default=0)
