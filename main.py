# main.py — CleanSky backend (FastAPI + OpenAQ + Open-Meteo)
# Run with: uvicorn main:app --reload

import os, random, requests
from datetime import datetime, timedelta
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Config
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
HEADERS = {"X-API-Key": OPENAQ_API_KEY} if OPENAQ_API_KEY else {}
OPENMETEO_BASE = "https://api.open-meteo.com/v1/forecast"

app = FastAPI(title="CleanSky API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Safe request wrapper
def safe_get(url, params=None, headers=None, timeout=10):
    try:
        r = requests.get(url, params=params or {}, headers=headers or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("[ERROR]", url, e)
        return None

@app.get("/")
def root():
    return {"message": "CleanSky backend running"}

# -------- Air Quality (OpenAQ) ----------
@app.get("/air-quality")
def air_quality(lat: float = Query(...), lon: float = Query(...)):
    url = "https://api.openaq.org/v3/locations"
    params = {"coordinates": f"{lat},{lon}", "radius": 20000, "limit": 5, "sort": "distance"}
    data = safe_get(url, params=params, headers=HEADERS)

    if not data or not data.get("results"):
        # fallback demo data
        return {
            "aggregated": {"pm25": 25, "pm10": 40, "no2": 20},
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "locations": [{
                "location": "Fallback Station",
                "coordinates": {"latitude": lat, "longitude": lon},
                "measurements": {"pm25": 25, "pm10": 40, "no2": 20}
            }]
        }

    results = data.get("results", [])
    vals = {"pm25": [], "pm10": [], "no2": []}
    locations_out = []

    for loc in results:
        coords = loc.get("coordinates") or {}
        measures = {}
        for p in loc.get("parameters", []):
            param = p.get("parameter")
            val = p.get("lastValue")
            if param in vals and val is not None:
                try:
                    vals[param].append(float(val))
                    measures[param] = val
                except:
                    pass
        locations_out.append({
            "location": loc.get("name") or loc.get("location") or "Unknown",
            "coordinates": coords,
            "measurements": measures
        })

    aggregated = {k: (sum(v)/len(v) if v else None) for k, v in vals.items()}
    return {"aggregated": aggregated, "last_updated": datetime.utcnow().isoformat() + "Z", "locations": locations_out}

# -------- Weather (Open-Meteo) ----------
@app.get("/weather")
def current_weather(lat: float, lon: float):
    params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"}
    data = safe_get(OPENMETEO_BASE, params=params)
    if not data or "current_weather" not in data:
        raise HTTPException(502, "Weather unavailable")
    return {"current_weather": data["current_weather"]}

# -------- Forecast (Open-Meteo) ----------
@app.get("/forecast")
def forecast(lat: float, lon: float, days: int = 14):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days
    }
    data = safe_get(OPENMETEO_BASE, params=params)
    if not data or "daily" not in data:
        # fallback: synthetic forecast
        base = datetime.utcnow()
        dates = [(base + timedelta(days=i)).date().isoformat() for i in range(days)]
        return {"daily": {
            "time": dates,
            "temperature_2m_max": [random.uniform(20, 35) for _ in dates],
            "temperature_2m_min": [random.uniform(10, 20) for _ in dates],
            "precipitation_sum": [random.uniform(0, 5) for _ in dates]
        }}
    return {"daily": data["daily"]}

# Serve frontend (static/index.html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
