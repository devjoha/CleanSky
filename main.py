# main.py — CleanSky backend (FastAPI + OpenAQ + Open-Meteo)
# Run with: uvicorn main:app --reload

import os, random, requests
from datetime import datetime, timedelta
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Config
OPENMETEO_BASE = "https://api.open-meteo.com/v1/forecast"

app = FastAPI(title="CleanSky API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class CacheControlMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		response = await call_next(request)
		response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		response.headers["Pragma"] = "no-cache"
		response.headers["Expires"] = "0"
		return response


app.add_middleware(CacheControlMiddleware)


# Safe request wrapper
def safe_get(url, params=None, headers=None, timeout=10):
	try:
		r = requests.get(url, params=params or {}, headers=headers or {}, timeout=timeout)
		r.raise_for_status()
		return r.json()
	except Exception as e:
		print("[ERROR]", url, e)
		return None


# -------- Air Quality (Open-Meteo) ----------
@app.get("/air-quality")
def air_quality(lat: float = Query(...), lon: float = Query(...)):
	url = "https://air-quality-api.open-meteo.com/v1/air-quality"
	params = {
		"latitude": lat,
		"longitude": lon,
		"current": "pm10,pm2_5,nitrogen_dioxide,european_aqi",
		"timezone": "auto"
	}
	data = safe_get(url, params=params)

	if not data or "current" not in data:
		return {
			"aggregated": {"pm25": None, "pm10": None, "no2": None},
			"last_updated": datetime.utcnow().isoformat() + "Z",
			"locations": []
		}

	current = data.get("current", {})
	pm25 = current.get("pm2_5")
	pm10 = current.get("pm10")
	no2 = current.get("nitrogen_dioxide")

	aggregated = {
		"pm25": pm25,
		"pm10": pm10,
		"no2": no2
	}

	location_name = f"Air Quality Station ({lat:.2f}, {lon:.2f})"

	locations_out = [{
		"location": location_name,
		"coordinates": {"latitude": lat, "longitude": lon},
		"measurements": {k: v for k, v in aggregated.items() if v is not None}
	}]

	return {
		"aggregated": aggregated,
		"last_updated": data.get("current", {}).get("time", datetime.utcnow().isoformat()) + "Z",
		"locations": locations_out if any(aggregated.values()) else []
	}


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

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=5000)
