# UrbanPulse Ultimate Dashboard

UrbanPulse Ultimate Dashboard is an immersive real-time smart city intelligence project.
It combines live weather, AQI, flight traffic, infrastructure signals, and an AI-style City Health Score in one interactive Streamlit application.

## Highlights

- Real weather integration (OpenWeather) with robust fallback data
- Real AQI integration (OpenWeather Air Pollution) with fallback data
- Live flight activity integration (OpenSky) with fallback data
- City Health Score and congestion analytics
- 3D visual dashboard with mobility arcs and globe view
- Time slider and optional live refresh mode

## Tech Stack

- Python
- Streamlit
- Plotly
- Pandas
- Requests
- SQLite (default) with optional MySQL backend

## Project Structure

```text
.
├── dashboard/
│   └── app.py
├── data_pipeline/
│   ├── airport.py
│   ├── aqi.py
│   ├── cities.py
│   ├── city_metrics.py
│   ├── flight.py
│   ├── population.py
│   └── weather.py
├── database/
│   └── schema.sql
├── main.py
├── utils.py
├── requirements.txt
├── runtime.txt
└── .env.example
```

## Quick Start

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Run pipeline snapshot:

```bash
python3 main.py
```

3. Start dashboard:

```bash
python3 -m streamlit run dashboard/app.py --server.port 8502
```

## Environment Variables

Copy `.env.example` to `.env` and configure if needed:

- `WEATHER_API_KEY` (optional)
- `AQI_API_KEY` (optional)
- `DB_BACKEND=sqlite` or `DB_BACKEND=mysql`
- `SQLITE_DB_PATH=urbanpulse.db`

If API keys are missing, the app still runs with deterministic mock data.

## Deployment (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. Create a new app on Streamlit Community Cloud.
3. Set app entrypoint to `dashboard/app.py`.
4. Add secrets if you want live API-backed data.
5. Deploy.

## Validation Commands

```bash
python3 main.py
python3 -m py_compile main.py utils.py dashboard/app.py data_pipeline/*.py
```

## Notes

- Local database `urbanpulse.db` is generated automatically.
- MySQL mode requires `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`.
