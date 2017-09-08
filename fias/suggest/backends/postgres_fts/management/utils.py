from django.db import connections
from django.db .backends.base.base import BaseDatabaseWrapper
from fias.config import DATABASE_ALIAS


connection = connections[DATABASE_ALIAS]  # type: BaseDatabaseWrapper


def trunc_index_table():
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE fias_addrobjindex RESTART IDENTITY")


def fill_index_table():
    sql = """
        WITH RECURSIVE PATH (aoguid, aolevel, scname, fullname, item_weight) AS (
          SELECT
            ao.aoguid,
            ao.aolevel,
            sn.socrname::TEXT AS scname,
            ao.shortname || ' ' || ao.formalname AS fullname,
            sn.item_weight
          FROM
            fias_addrobj AS ao INNER JOIN fias_socrbase AS sn
              ON (sn.scname = ao.shortname AND sn.level = ao.aolevel)
          WHERE
            ao.aolevel = 1 AND ao.livestatus = TRUE
          UNION
          SELECT
            child.aoguid, child.aolevel,
            PATH.scname::TEXT || ', ' || sn.socrname::TEXT AS scname,
            PATH.fullname || ', ' || child.shortname || ' ' || child.formalname AS fullname,
            sn.item_weight
          FROM
            fias_addrobj AS child INNER JOIN fias_socrbase AS sn
              ON (sn.scname = child.shortname AND sn.level = child.aolevel)
            , PATH
          WHERE child.parentguid = PATH.aoguid AND child.livestatus = TRUE
        )
        INSERT INTO fias_addrobjindex (
          aoguid, aolevel, scname, fullname, 
          item_weight, search_vector)
        SELECT 
          aoguid, aolevel, scname, fullname, item_weight, 
          to_tsvector('russian', fullname) 
        FROM PATH;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)


def create_gin_index():
    with connection.cursor() as cursor:
        cursor.execute("DROP INDEX IF EXISTS fias_addrobjindex_idx")
        cursor.execute("CREATE INDEX fias_addrobjindex_idx "
                       "ON fias_addrobjindex USING GIN (search_vector)")
