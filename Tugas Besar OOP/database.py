import sqlite3
import pandas as pd
from konfigurasi import DB_PATH
from model import OrderInventaris

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None

def execute_query(query, params=()):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("ERROR [DB]", e)
        return None
    finally:
        conn.close()

def fetch_query(query, params=(), fetch_all=True):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    finally:
        conn.close()

def get_dataframe(query, params=()):
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
