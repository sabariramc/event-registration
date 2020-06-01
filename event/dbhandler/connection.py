from flask import g, current_app


def teardown_request(exc):
    if hasattr(g, "mysql_dbs"):
        try:
            g.mysql_cnx.close()
        except Exception:
            pass


def get_db():
    if not hasattr(g, "mysql_db"):
        g.mysql_cnx = current_app.connection_pool.get_connection()
    return g.mysql_cnx
