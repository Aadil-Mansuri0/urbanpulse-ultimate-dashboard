# Modified by Aadil Mansuri
from __future__ import annotations

from datetime import datetime
import math
from pathlib import Path
import sys
import time

import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_pipeline.city_metrics import build_city_metrics
from data_pipeline.cities import get_available_cities


st.set_page_config(page_title="UrbanPulse Ultimate", page_icon="🌍", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

    :root {
        --bg-1: #f7efe5;
        --bg-2: #f3d6b2;
        --card: rgba(255, 255, 255, 0.74);
        --text: #10212f;
        --accent: #e06b2f;
        --accent-2: #007c7c;
    }

    .stApp {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text);
        background:
            radial-gradient(1000px 500px at 15% 0%, rgba(0, 124, 124, 0.20), transparent 70%),
            radial-gradient(900px 480px at 100% 10%, rgba(224, 107, 47, 0.22), transparent 60%),
            linear-gradient(165deg, var(--bg-1), var(--bg-2));
    }

    .hero {
        padding: 14px 18px;
        border-radius: 18px;
        background: var(--card);
        border: 1px solid rgba(16, 33, 47, 0.10);
        backdrop-filter: blur(6px);
        box-shadow: 0 10px 34px rgba(16, 33, 47, 0.14);
        margin-bottom: 10px;
    }

    .kpi {
        border-radius: 14px;
        border: 1px solid rgba(16, 33, 47, 0.09);
        background: rgba(255, 255, 255, 0.82);
        padding: 10px 14px;
    }

    .kpi label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #5c6f7b;
        font-family: 'IBM Plex Mono', monospace;
    }

    .kpi h3 {
        margin: 4px 0 0 0;
        font-weight: 700;
        color: #122738;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero">
      <h1 style="margin:0;">UrbanPulse Ultimate Command Center</h1>
      <p style="margin:6px 0 0 0;">Immersive city intelligence with weather, AQI, flights, and AI health scoring. Last sync: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

available_cities = get_available_cities()
with st.sidebar:
    st.header("Control Panel")
    selected_cities = st.multiselect(
        "Cities",
        options=available_cities,
        default=available_cities[:4],
    )
    hour_slider = st.slider("Time Slider", 0, 23, datetime.now().hour)
    live_mode = st.toggle("Live Updating", value=False)
    refresh_seconds = st.slider("Live Refresh (seconds)", 5, 120, 20)

if not selected_cities:
    st.warning("Select at least one city to render dashboard.")
    st.stop()

metrics = build_city_metrics(selected_cities, hour_override=hour_slider)

if metrics.empty:
    st.error("No metrics available right now. Please retry.")
    st.stop()

mean_score = metrics["city_health_score"].mean()
mean_aqi = metrics["aqi"].mean()
total_flights = int(metrics["flights"].sum())
mean_temp = metrics["temp"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi'><label>Avg Health Score</label><h3>{mean_score:.1f}</h3></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi'><label>Avg AQI</label><h3>{mean_aqi:.0f}</h3></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi'><label>Live Flights</label><h3>{total_flights}</h3></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi'><label>Mean Temperature</label><h3>{mean_temp:.1f}C</h3></div>", unsafe_allow_html=True)


def build_air_traffic_3d(frame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=frame["lon"],
            y=frame["lat"],
            z=frame["flights"],
            mode="markers+text",
            text=frame["city"],
            textposition="top center",
            marker={
                "size": 9,
                "color": frame["city_health_score"],
                "colorscale": "Tealgrn",
                "line": {"width": 1, "color": "#0a2433"},
                "showscale": True,
                "colorbar": {"title": "Health"},
            },
            name="Cities",
        )
    )

    phase = math.sin(hour_slider * math.pi / 12)
    for i in range(len(frame)):
        for j in range(i + 1, len(frame)):
            lift = (frame.iloc[i]["flights"] + frame.iloc[j]["flights"]) / 3.8
            arc_mid = lift + abs(phase) * 24
            fig.add_trace(
                go.Scatter3d(
                    x=[frame.iloc[i]["lon"], (frame.iloc[i]["lon"] + frame.iloc[j]["lon"]) / 2, frame.iloc[j]["lon"]],
                    y=[frame.iloc[i]["lat"], (frame.iloc[i]["lat"] + frame.iloc[j]["lat"]) / 2, frame.iloc[j]["lat"]],
                    z=[frame.iloc[i]["flights"] * 0.6, arc_mid, frame.iloc[j]["flights"] * 0.6],
                    mode="lines",
                    line={"width": 3, "color": "rgba(224,107,47,0.55)"},
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    fig.update_layout(
        margin={"l": 0, "r": 0, "b": 0, "t": 30},
        title="3D Air Mobility Grid",
        scene={
            "xaxis_title": "Longitude",
            "yaxis_title": "Latitude",
            "zaxis_title": "Flight Intensity",
            "bgcolor": "rgba(255,255,255,0.6)",
        },
    )
    return fig


def build_globe_map(frame):
    return go.Figure(
        go.Scattergeo(
            lon=frame["lon"],
            lat=frame["lat"],
            text=frame["city"]
            + "<br>Temp: "
            + frame["temp"].round(1).astype(str)
            + "C<br>AQI: "
            + frame["aqi"].astype(str),
            mode="markers+text",
            marker={
                "size": frame["city_health_score"] / 5,
                "color": frame["aqi"],
                "colorscale": "Turbo",
                "line": {"width": 1, "color": "#162f41"},
                "showscale": True,
                "colorbar": {"title": "AQI"},
            },
            textposition="top center",
            name="Cities",
        )
    ).update_layout(
        title="Earth View (Operational Lens)",
        geo={
            "projection": {"type": "orthographic"},
            "showland": True,
            "landcolor": "rgb(232, 230, 214)",
            "showocean": True,
            "oceancolor": "rgb(177, 214, 242)",
            "lataxis": {"range": [6, 37]},
            "lonaxis": {"range": [66, 92]},
        },
        margin={"l": 0, "r": 0, "b": 0, "t": 38},
    )


left, right = st.columns([1.6, 1])
with left:
    st.plotly_chart(build_air_traffic_3d(metrics), use_container_width=True)
with right:
    st.plotly_chart(build_globe_map(metrics), use_container_width=True)

bottom_l, bottom_r = st.columns([1.2, 1])
with bottom_l:
    score_fig = go.Figure()
    score_fig.add_trace(
        go.Bar(
            x=metrics["city"],
            y=metrics["city_health_score"],
            name="Health Score",
            marker_color="#007c7c",
        )
    )
    score_fig.add_trace(
        go.Scatter(
            x=metrics["city"],
            y=metrics["aqi"],
            yaxis="y2",
            mode="lines+markers",
            name="AQI",
            line={"color": "#e06b2f", "width": 3},
        )
    )
    score_fig.update_layout(
        title="Health Score vs AQI",
        yaxis={"title": "Health Score"},
        yaxis2={"title": "AQI", "overlaying": "y", "side": "right"},
        margin={"l": 0, "r": 0, "b": 0, "t": 38},
    )
    st.plotly_chart(score_fig, use_container_width=True)

with bottom_r:
    best = metrics.iloc[0]
    radar = go.Figure(
        data=[
            go.Scatterpolar(
                r=[
                    min(100, best["city_health_score"]),
                    max(0, 100 - best["aqi"] * 0.4),
                    max(0, 100 - best["congestion_index"]),
                    min(100, best["temp_next_hour"] * 2.5),
                    min(100, best["airports"] * 30),
                ],
                theta=["Health", "Air", "Mobility", "Temp Trend", "Infra"],
                fill="toself",
                name=best["city"],
                line={"color": "#e06b2f"},
                fillcolor="rgba(224,107,47,0.25)",
            )
        ]
    )
    radar.update_layout(
        title=f"Top City Profile: {best['city']}",
        polar={"radialaxis": {"visible": True, "range": [0, 100]}},
        margin={"l": 0, "r": 0, "b": 0, "t": 38},
    )
    st.plotly_chart(radar, use_container_width=True)

st.subheader("Live Metrics Table")
st.dataframe(
    metrics[
        [
            "rank",
            "city",
            "temp",
            "temp_next_hour",
            "weather",
            "aqi",
            "aqi_band",
            "flights",
            "congestion_index",
            "city_health_score",
            "score_label",
            "weather_source",
            "aqi_source",
            "flights_source",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

if live_mode:
    st.sidebar.success(f"Live mode enabled. Auto-refresh every {refresh_seconds}s")
    time.sleep(refresh_seconds)
    st.rerun()
