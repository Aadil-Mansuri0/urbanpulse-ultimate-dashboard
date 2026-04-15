# UrbanPulse Ultimate

UrbanPulse Ultimate is an immersive city intelligence dashboard built with Python and Streamlit.
It combines weather, AQI, flight activity, and infrastructure signals to generate a City Health Score.

## Features

- Real weather data from OpenWeather with safe fallback data
- Real AQI integration with safe fallback data
- Live flight traffic estimation from OpenSky with safe fallback data
- AI-style City Health Score and congestion index
- Immersive 3D dashboard with:
  - 3D mobility grid
  - Globe operational view
  - Time slider
  - Optional live auto-refresh

## Project Structure

- dashboard/app.py: Streamlit dashboard entrypoint
- data_pipeline/: Data connectors and metrics computation
- database/schema.sql: SQLite schema for metrics logging
- main.py: Snapshot pipeline runner
- utils.py: Database utilities

## Quick Start (Local)

1. Install dependencies:

   python3 -m pip install -r requirements.txt

2. Run snapshot pipeline:

   python3 main.py

3. Start dashboard:

   python3 -m streamlit run dashboard/app.py --server.port 8502

## Environment Variables

Copy .env.example to .env and update values if needed.

- WEATHER_API_KEY: OpenWeather API key (optional)
- AQI_API_KEY: Optional AQI key. If not set, WEATHER_API_KEY is reused for AQI endpoint.
- DB_BACKEND: sqlite (default) or mysql
- SQLITE_DB_PATH: SQLite file path (default: urbanpulse.db)

If API keys are missing, the app still runs with deterministic mock data.

## Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. Create a new app in Streamlit Community Cloud.
3. Set main file path to: dashboard/app.py
4. Add secrets if you want live APIs:
   - WEATHER_API_KEY
   - AQI_API_KEY (optional)
5. Deploy.

## Validation Commands

- python3 main.py
- python3 -m py_compile main.py utils.py dashboard/app.py data_pipeline/*.py

## Notes

- SQLite database file urbanpulse.db is generated automatically.
- For MySQL mode, set DB_BACKEND=mysql and provide MYSQL_* variables in environment.
