import psycopg
from psycopg import sql

def create_db_if_missing(db_name, user, password, host="127.0.0.1", port=5432):
    with psycopg.connect(dbname="postgres", user=user, password=password, host=host, port=port, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
            if cur.fetchone() is None:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Database {db_name} created")
