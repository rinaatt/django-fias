def filter_chelyabinsk_region(item):
    """
    Всегда разрешает импорт записи
    :param item:
    :return item or None:
    """
    if item.regioncode == '74':
        return item
