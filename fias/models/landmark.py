# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from ..fields import UUIDField
from ..app import APP_LABEL
from .addrobj import AddrObj
from .common import Common

__all__ = ['LandMark']


class LandMark(Common):
    """
    Описание мест расположения имущественных объектов
    """
    class Meta:
        app_label = APP_LABEL
        verbose_name = 'Место расположения имущественного объекта'
        verbose_name_plural = 'Места расположения имущественных объектов'

    landid = UUIDField('Уникальный идентификатор записи ориентира', unique=True)
    landguid = UUIDField('Глобальный уникальный идентификатор ориентира', primary_key=True)
    aoguid = models.ForeignKey(AddrObj, verbose_name='Идентификатор записи родительского объекта',
                               help_text='(улица, город, населенный пункт и т.п.)')

    location = models.TextField('Месторасположение ориентира')

    cadnum = models.CharField('Кадастровый номер', max_length=100, blank=True, null=True)
