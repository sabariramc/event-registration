import json
import time

from .connection import get_db

from ..utility import get_json_serialized_obj


def execute_sql_statement(sql_stmt: str, parameters: dict = None, is_insert=False, sql_cnx=None):
    """
    To execute a sql statement. Internally used by update and insert record functions
    the parameters can be of any python supported type (int,float,Decimal,dict,list,date,datetime,....)
    :param sql_stmt: SQL query to execute in case of a parameterized sql use %(columnName)s over %s
    :param parameters: parameters  - dict for %(columnName)s and tuple for %s
    :param is_insert: In case the query is a insert query
    :param cnx_db: In case the application uses multiple db then this will be useful
    :return: in case of select the selection set and in case of insert the id object
    """
    if isinstance(parameters, dict):
        for key, value in parameters.items():
            if isinstance(value, dict) or isinstance(value, list):
                serialized_obj = get_json_serialized_obj(value)
                parameters[key] = json.dumps(serialized_obj)
    out = []
    st = time.time()
    cnx = sql_cnx if sql_cnx else get_db()
    p_cur = cnx.cursor()
    try:
        ret_value = p_cur.execute(sql_stmt, parameters)
        if is_insert:
            out.append({"id": p_cur.lastrowid})
        else:
            if p_cur.description:
                column_name_list = list(map(lambda a: a[0], p_cur.description))
                out = list(map(lambda a: dict(zip(column_name_list, a)), p_cur.fetchall()))
            else:
                if ret_value == -1:
                    out = []
        rows_affected = p_cur.rowcount
    finally:
        p_cur.close()
    execution_time = time.time() - st
    return out
