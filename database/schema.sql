CREATE TABLE IF NOT EXISTS city_metrics_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    weather TEXT NOT NULL,
    aqi INTEGER NOT NULL,
    aqi_band TEXT NOT NULL,
    flights_active INTEGER NOT NULL,
    avg_altitude REAL NOT NULL,
    airports INTEGER NOT NULL,
    population INTEGER NOT NULL,
    congestion_index REAL NOT NULL,
    city_health_score REAL NOT NULL,
    weather_source TEXT NOT NULL,
    aqi_source TEXT NOT NULL,
    flights_source TEXT NOT NULL
);
