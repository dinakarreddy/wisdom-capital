import psycopg2


def get_connection():
    conn = psycopg2.connect("dbname=nse user=nse password=nse port=25432")
    return conn
