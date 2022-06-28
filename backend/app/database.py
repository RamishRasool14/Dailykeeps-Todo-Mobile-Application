import psycopg2
import os


class Database:
    def __init__(self, existing_db=True) -> None:
        self._conn = None
        self.config = {
            "DBNAME": os.getenv("DBNAME")
            if os.getenv("TESTING") == "0"
            else os.getenv("DBNAMETEST"),
            "DBPASS": os.getenv("DBPASS"),
            "USERNAME": os.getenv("USERNAME"),
            "SCHEMAPATH": os.getenv("SCHEMAPATH"),
            "JWTSECRET": os.getenv("JWTSECRET"),
            "DBPUBLICIP": os.getenv("DBPUBLICIP"),
        }
        if existing_db:
            self.connect()
        else:
            self._drop_and_create_new_db()

    def __exit__(self, typ, value, traceback):
        self.close()

    def __enter__(self):
        return self

    def connect(self):
        self._conn = psycopg2.connect(
            "dbname={} user={} password={} host={}".format(
                self.config["DBNAME"],
                self.config["USERNAME"],
                self.config["DBPASS"],
                self.config["DBPUBLICIP"],
            )
        )
        self._cur = self._conn.cursor()

    def cursor(self):
        return self._cur

    def commit(self):
        self._conn.commit()

    def execute(self, query, *args):
        self._cur.execute(query, args)
        return self._cur

    def rollback(self):
        self._conn.rollback()

    def _drop_db(self):
        os.system("dropdb {}".format(self.config["DBNAME"]))

    def _create_db(self):
        os.system("createdb {}".format(self.config["DBNAME"]))

    def _create_tables_from_schema(self):
        os.system(
            "psql {} -af {}".format(self.config["DBNAME"], self.config["SCHEMAPATH"])
        )

    def _drop_and_create_new_db(self):
        self._drop_db()
        self._create_db()
        self._create_tables_from_schema()

    def close(self):
        self._cur.close()
        self._conn.close()
