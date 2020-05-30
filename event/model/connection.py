from flask import g, current_app


def teardown_request(prefix="mysql"):
    if hasattr(g, "mysql_dbs"):
        try:
            if prefix in g.mysql_dbs and g.mysql_dbs[prefix].open:
                g.mysql_dbs[prefix].close()
                g.mysql_dbs.pop(prefix)
        except Exception:
            pass


def get_db(prefix="mysql"):
    if not hasattr(g, "mysql_db"):
        g.mysql_dbs = dict()
    if prefix not in g.mysql_dbs:
        g.mysql_dbs[prefix] = current_app.connection_pool.get(prefix).get_connection()
    return g.mysql_dbs.get(prefix)
