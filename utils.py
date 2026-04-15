# Modified by Aadil Mansuri
from __future__ import annotations

import os
import sqlite3

import pandas as pd
import pymysql


def get_connection():
    backend = os.getenv("DB_BACKEND", "sqlite").lower()
    if backend == "mysql":
        return pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "urbanpulse"),
        )

    db_path = os.getenv("SQLITE_DB_PATH", "urbanpulse.db")
    return sqlite3.connect(db_path)


def initialize_database(schema_path: str = "database/schema.sql") -> None:
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
    finally:
        conn.close()


def save_metrics(df: pd.DataFrame, table_name: str = "city_metrics_log") -> None:
    if df.empty:
        return

    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            cols = [
                "city",
                "observed_at",
                "temp",
                "weather",
                "aqi",
                "aqi_band",
                "flights",
                "avg_altitude",
                "airports",
                "population",
                "congestion_index",
                "city_health_score",
                "weather_source",
                "aqi_source",
                "flights_source",
            ]
            rename_map = {
                "temp": "temperature_c",
                "flights": "flights_active",
            }
            upload_df = df[cols].rename(columns=rename_map)
            upload_df.to_sql(table_name, conn, if_exists="append", index=False)
    finally:
        conn.close()


def fetch_data(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()
